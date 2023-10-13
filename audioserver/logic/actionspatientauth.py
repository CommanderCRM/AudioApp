import os
from sqlmodel import Session, create_engine, select
from .actions import select_patient_by_key
from .tables import PatientTable, TokenObject
from .actionsauth import hash_gost_3411, validate_pass, generate_jwt

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

def change_temporary_password(card_number, constant_password, temporary_password):
    """Смена временного пароля на постоянный"""
    if (select_patient_by_key(card_number) and constant_password != temporary_password
    and check_temp_pass_equality(card_number, temporary_password)
    and validate_pass(constant_password)):
        hashed_const = hash_gost_3411(constant_password)

        with Session(engine) as session:
            patient = session.query(PatientTable).filter(PatientTable.card_number == card_number).first()
            if patient:
                patient.temporary_password = ""
                patient.constant_password = hashed_const
                patient.is_password_changed = 1
                session.commit()

        short_jwt = generate_jwt(card_number, 'patient', 'short')
        long_jwt = generate_jwt(card_number, 'patient', 'long')

        return TokenObject(access_token=short_jwt, refresh_token=long_jwt)

    return False