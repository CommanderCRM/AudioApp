import os
from pygost.gost34112012 import GOST34112012
from sqlmodel import Session, create_engine, select
from .actions import select_patient_by_key
from .tables import PatientTable

if os.getenv('TESTING'):
    engine = create_engine('sqlite:///sqlite3.db')
else:
    engine = create_engine("postgresql://postgres:postgres@sql:5432/postgres", echo=True)

def validate_const_pass(constant_password):
    """Валидация постоянного пароля"""
    special_chars=r"!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    numbers="01234567890"

    if (any(c in special_chars for c in constant_password)
        and any(c in numbers for c in constant_password)):
        return True

    return False

def check_temp_pass_equality(card_number, temporary_password):
    """Проверка совпадения временного и постоянного паролей"""
    with Session(engine) as session:
        patient = session.exec(select(PatientTable)
                               .where(PatientTable.card_number == card_number)).first()

        return temporary_password == patient.temporary_password

def hash_const_pass(constant_password):
    """Хэширование постоянного пароля по ГОСТ 34.11-2018 (256 бит)"""
    m = GOST34112012(digest_size=256)
    pass_bytes = str.encode(constant_password)
    m.update(pass_bytes)

    return m.hexdigest()

def change_temporary_password(card_number, constant_password, temporary_password):
    """Смена временного пароля на постоянный"""
    if (select_patient_by_key(card_number) and constant_password != temporary_password
    and check_temp_pass_equality(card_number, temporary_password)
    and validate_const_pass(constant_password)):
        hashed_const = hash_const_pass(constant_password)

        with Session(engine) as session:
            patient = session.query(PatientTable).filter(PatientTable.card_number == card_number).first()
            if patient:
                patient.temporary_password = ""
                patient.constant_password = hashed_const
                patient.is_password_changed = 1
                session.commit()
