from sqlmodel import Session, create_engine, select
from .tables import PatientTable

engine = create_engine("postgresql://postgres:postgres@sql:5432/postgres", echo=True)

def insert_patient(patient: PatientTable):
    """Запись пациента в БД"""
    with Session(engine) as session:
        session.add(patient)
        session.commit()
        session.refresh(patient)
        return

def select_all_patients():
    """Получение всех пациентов из БД"""
    with Session(engine) as session:
        patients = session.exec(select(PatientTable)).all()
        return patients
