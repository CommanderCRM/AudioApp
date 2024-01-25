import os
from sqlmodel import Session, create_engine, select
from .tables import PatientTable, TokenObject
from .actions import select_patient_by_key
from .secactions import hash_gost_3411, validate_pass
from .actionsauth import create_two_tokens

JWT_KEY = "8694c19e-17d7-4479-88eb-402c07fea387" # nosec

if os.getenv('TESTING'):
    engine = create_engine('sqlite:///sqlite3.db')
else:
    engine = create_engine("postgresql://webpegas:webpegas@sql:5432/postgres", echo=True)

def check_temp_pass_equality(card_number, temporary_password):
    """Проверка совпадения временного и постоянного паролей"""
    with Session(engine) as session:
        patient = session.exec(select(PatientTable)
                               .where(PatientTable.card_number == card_number)).first()

        temporary_password_hash = hash_gost_3411(temporary_password)

        return temporary_password_hash == patient.temporary_password

def change_temporary_password(card_number, constant_password, temporary_password):
    """Смена временного пароля на постоянный"""
    if select_patient_by_key(card_number) and constant_password != temporary_password:
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

        short_jwt, long_jwt = create_two_tokens(card_number, 'patient')
        return TokenObject(access_token=short_jwt, refresh_token=long_jwt)

    return False
