import os
import datetime
import calendar
import uuid
import jwt
from sqlmodel import Session, create_engine
from .actions import select_patient_by_key, select_doctor_by_key, select_specialist_by_key
from .tables import PatientTable, TokenObject, RefreshTokenTable, DoctorTable, SpecialistTable
from .secactions import hash_gost_3411, generate_jwt

JWT_KEY = "8694c19e-17d7-4479-88eb-402c07fea387" # nosec

if os.getenv('TESTING'):
    engine = create_engine('sqlite:///sqlite3.db')
else:
    engine = create_engine("postgresql://postgres:postgres@sql:5432/postgres", echo=True)

def create_two_tokens(card_number, role):
    """Создание пары токенов"""
    generated_uuid = str(uuid.uuid4())
    short_jwt = generate_jwt(generated_uuid, card_number, role, 'short')
    long_jwt = generate_jwt(generated_uuid, card_number, role, 'long')

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

def check_token(token_for_check):
    """Проверка токена"""
    decoded_jwt = jwt.decode(token_for_check, JWT_KEY, algorithms="HS256")

    token = decoded_jwt['uuid']
    username = decoded_jwt['user']
    role = decoded_jwt['role']

    current_datetime = datetime.datetime.utcnow()
    current_utcstamp = calendar.timegm(current_datetime.utctimetuple())

    with Session(engine) as session:
        refresh_token = session.query(RefreshTokenTable).\
                                filter(RefreshTokenTable.token == token).first()
        if refresh_token:
            refresh_token_exp = refresh_token.exp

    if role == 'patient':
        if (select_patient_by_key(username)
            and current_utcstamp <= refresh_token_exp):
            return True
    elif role == 'doctor':
        if (select_doctor_by_key(username)
            and current_utcstamp <= refresh_token_exp):
            return True
    elif role == 'specialist':
        if (select_specialist_by_key(username)
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

def get_role_from_token(token):
    """Получение роли из токена"""
    decoded_jwt = jwt.decode(token, JWT_KEY, algorithms="HS256")

    role = decoded_jwt['role']

    return role

def check_data_and_login(username, constant_password):
    """Проверка данных и логин пользователя"""
    if select_patient_by_key(username):
        constant_password_hash = hash_gost_3411(constant_password)
        role = 'patient'
    elif select_doctor_by_key(username):
        constant_password_hash = hash_gost_3411(constant_password)
        role = 'doctor'
    elif select_specialist_by_key(username):
        constant_password_hash = hash_gost_3411(constant_password)
        role = 'specialist'

    with Session(engine) as session:
        if role == 'patient':
            patient_const_pass = session.query(PatientTable).\
                                        filter(PatientTable.card_number == username,
                                                PatientTable.constant_password == constant_password_hash).\
                                        first()
            if patient_const_pass:
                short_jwt, long_jwt = create_two_tokens(username, 'patient')
                return TokenObject(access_token=short_jwt, refresh_token=long_jwt)
        elif role == 'doctor':
            doctor_const_pass = session.query(DoctorTable).\
                                        filter(DoctorTable.username == username,
                                                DoctorTable.password == constant_password_hash).\
                                        first()
            if doctor_const_pass:
                short_jwt, long_jwt = create_two_tokens(username, 'doctor')
                return TokenObject(access_token=short_jwt, refresh_token=long_jwt)
        elif role == 'specialist':
            specialist_const_pass = session.query(SpecialistTable).\
                                        filter(SpecialistTable.username == username,
                                                SpecialistTable.password == constant_password_hash).\
                                        first()
            if specialist_const_pass:
                short_jwt, long_jwt = create_two_tokens(username, 'specialist')
                return TokenObject(access_token=short_jwt, refresh_token=long_jwt)

    return False

def change_const_password(username, old_password, new_password, role):
    """Смена постоянного пароля на новый"""
    if role == 'patient':
        if select_patient_by_key(username):
            old_pwd_hash = hash_gost_3411(old_password)
            new_pwd_hash = hash_gost_3411(new_password)
    elif role == 'doctor':
        if select_doctor_by_key(username):
            old_pwd_hash = hash_gost_3411(old_password)
            new_pwd_hash = hash_gost_3411(new_password)
    elif role == 'specialist':
        if select_specialist_by_key(username):
            old_pwd_hash = hash_gost_3411(old_password)
            new_pwd_hash = hash_gost_3411(new_password)

    with Session(engine) as session:
        if role == 'patient':
            patient_const_pass = session.query(PatientTable).\
                                        filter(PatientTable.card_number == username,
                                                PatientTable.constant_password == old_pwd_hash).first()
            if patient_const_pass:
                session.query(PatientTable).\
                    filter(PatientTable.card_number == username,
                        PatientTable.constant_password == old_pwd_hash).\
                    update({'constant_password': new_pwd_hash})
                session.commit()
                return
        elif role == 'doctor':
            doctor_const_pass = session.query(DoctorTable).\
                                        filter(DoctorTable.username == username,
                                                DoctorTable.password == old_pwd_hash).\
                                        first()
            if doctor_const_pass:
                session.query(DoctorTable).\
                    filter(DoctorTable.username == username,
                        DoctorTable.password == old_pwd_hash).\
                    update({'password': new_pwd_hash})
                session.commit()
                return
        elif role == 'specialist':
            specialist_const_pass = session.query(SpecialistTable).\
                                        filter(SpecialistTable.username == username,
                                                SpecialistTable.password == old_pwd_hash).\
                                        first()
            if specialist_const_pass:
                session.query(SpecialistTable).\
                    filter(SpecialistTable.username == username,
                        SpecialistTable.password == old_pwd_hash).\
                    update({'password': new_pwd_hash})
                session.commit()
                return
