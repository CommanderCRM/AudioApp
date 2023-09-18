from sqlmodel import Session, create_engine, select
from .tables import PatientTable, ShortPatientModel

engine = create_engine("postgresql://postgres:postgres@sql:5432/postgres", echo=True)

def insert_patient(patient: PatientTable):
    """Запись пациента в БД"""
    with Session(engine) as session:
        session.add(patient)
        session.commit()
        session.refresh(patient)
        return

def select_all_patients():
    """Получение всех пациентов (короткая модель) из БД"""
    with Session(engine) as session:
        patients = session.query(PatientTable).with_entities(PatientTable.full_name,
                                                             PatientTable.date_of_birth,
                                                             PatientTable.gender,
                                                             PatientTable.medical_card_number).all()
        return patients

def select_patient_by_key(medical_card_number: str):
    """Получение пациента по ключу"""
    with Session(engine) as session:
        patient = session.exec(select(PatientTable).where(PatientTable.medical_card_number == medical_card_number)).first()
        return bool(patient)

def update_patient(medical_card_number: str, patient_update: ShortPatientModel):
    """Обновление информации o пациенте в БД (короткая модель)"""
    with Session(engine) as session:
        statement = select(PatientTable).where(PatientTable.medical_card_number == medical_card_number)
        patient = session.exec(statement).first()
        if patient:
            update_fields = ["full_name", "date_of_birth", "gender", "medical_card_number"]
            for var in update_fields:
                value = getattr(patient_update, var, None)
                if value is None:
                    return None  # Если нет обязательного поля
                setattr(patient, var, value)
            session.merge(patient)
            session.commit()
            session.refresh(patient)
            return
        return None

def delete_patient(medical_card_number: str):
    """Удаление пациента из БД"""
    with Session(engine) as session:
        patient = session.query(PatientTable).filter(PatientTable.medical_card_number == medical_card_number).first()
        if patient is not None:
            session.delete(patient)
            session.commit()
        return
