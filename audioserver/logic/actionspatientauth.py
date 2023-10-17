import os
import datetime
import calendar
import uuid
import jwt
from sqlmodel import Session, create_engine, select
from .actions import select_patient_by_key
from .tables import PatientTable, TokenObject, RefreshTokenTable
from .actionsauth import hash_gost_3411, validate_pass, generate_jwt

JWT_KEY = "8694c19e-17d7-4479-88eb-402c07fea387" # nosec

if os.getenv('TESTING'):
    engine = create_engine('sqlite:///sqlite3.db')
else:
    engine = create_engine("postgresql://postgres:postgres@sql:5432/postgres", echo=True)

def check_temp_pass_equality(card_number, temporary_password):
    """Проверка совпадения временного и постоянного паролей"""
    with Session(engine) as session:
        patient = session.exec(select(PatientTable)
                               .where(PatientTable.card_number == card_number)).first()

        temporary_password_hash = hash_gost_3411(temporary_password)

        return temporary_password_hash == patient.temporary_password

def create_two_tokens(card_number):
    """Создание пары токенов"""
    generated_uuid = str(uuid.uuid4())
    short_jwt = generate_jwt(generated_uuid, card_number, 'patient', 'short')
    long_jwt = generate_jwt(generated_uuid, card_number, 'patient', 'long')

    # Сохранение токена обновления в БД
    with Session(engine) as session:
        decoded_long_jwt = jwt.decode(long_jwt, JWT_KEY, algorithms="HS256")
        refresh_token_table = RefreshTokenTable(
            token=decoded_long_jwt['uuid'],
            username=decoded_long_jwt['user'],
            exp=decoded_long_jwt['exp'],
            role=decoded_long_jwt['role']
        )
        session.add(refresh_token_table)
        session.commit()

    return short_jwt, long_jwt

def delete_refresh_token(token_uuid):
    """Удаление токена обновления из БД"""
    with Session(engine) as session:
        token_to_delete = session.query(RefreshTokenTable).\
                                  filter(RefreshTokenTable.token == token_uuid).first()
        session.delete(token_to_delete)
        session.commit()

def change_temporary_password(card_number, constant_password, temporary_password):
    """Смена временного пароля на постоянный"""
    if (select_patient_by_key(card_number) and constant_password != temporary_password
    and check_temp_pass_equality(card_number, temporary_password)
    and validate_pass(constant_password)):
        hashed_const = hash_gost_3411(constant_password)

        # Непосредственная смена пароля
        with Session(engine) as session:
            patient = session.query(PatientTable).\
                      filter(PatientTable.card_number == card_number).first()
            if patient:
                patient.temporary_password = "" # nosec
                patient.constant_password = hashed_const
                patient.is_password_changed = 1
                session.commit()

        short_jwt, long_jwt = create_two_tokens(card_number)
        return TokenObject(access_token=short_jwt, refresh_token=long_jwt)

    return False

def check_token(token_for_check):
    """Проверка токена"""
    decoded_jwt = jwt.decode(token_for_check, JWT_KEY, algorithms="HS256")

    token=decoded_jwt['uuid']
    username = decoded_jwt['user']

    current_datetime = datetime.datetime.utcnow()
    current_utcstamp = calendar.timegm(current_datetime.utctimetuple())

    with Session(engine) as session:
        refresh_token = session.query(RefreshTokenTable).\
                                filter(RefreshTokenTable.token == token).first()
        if refresh_token:
            refresh_token_exp = refresh_token.exp

    if (select_patient_by_key(username) and decoded_jwt['role'] == 'patient'
        and current_utcstamp <= refresh_token_exp):
        return True

    return False

def get_username_from_token(token):
    """Получение имени пользователя из токена"""
    decoded_jwt = jwt.decode(token, JWT_KEY, algorithms="HS256")

    username = decoded_jwt['user']

    return username

def get_uuid_from_token(token):
    """Получение UUID из токена"""
    decoded_jwt = jwt.decode(token, JWT_KEY, algorithms="HS256")

    token_uuid = decoded_jwt['uuid']

    return token_uuid

def check_patient_and_login(card_number, constant_password):
    """Проверка данных и логин пациента"""
    if select_patient_by_key(card_number):
        constant_password_hash = hash_gost_3411(constant_password)

    with Session(engine) as session:
        patient_const_pass = session.query(PatientTable).\
                                     filter(PatientTable.card_number == card_number,
                                            PatientTable.constant_password == constant_password_hash).\
                                     first()
        if patient_const_pass:
            short_jwt, long_jwt = create_two_tokens(card_number)
            return TokenObject(access_token=short_jwt, refresh_token=long_jwt)

    return False

def change_const_patient_password(card_number, old_password, new_password):
    """Смена постоянного пароля пациента на новый"""
    if select_patient_by_key(card_number):
        old_pwd_hash = hash_gost_3411(old_password)
        new_pwd_hash = hash_gost_3411(new_password)

    with Session(engine) as session:
        patient_const_pass = session.query(PatientTable).\
                                     filter(PatientTable.card_number == card_number,
                                            PatientTable.constant_password == old_pwd_hash).first()
        if patient_const_pass:
            session.query(PatientTable).\
                filter(PatientTable.card_number == card_number,
                       PatientTable.constant_password == old_pwd_hash).\
                update({'constant_password': new_pwd_hash})
            session.commit()
            return
