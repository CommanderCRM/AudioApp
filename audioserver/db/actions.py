from sqlmodel import Session, create_engine, select
from models.models import Patient
from .tables import PatientTable

engine = create_engine("postgresql://postgres:postgres@sql:5432/postgres")

def insert_patient(patient: PatientTable):
    """Запись пациента в БД"""
    #patient_row = PatientTable(**patient.dict())
    with Session(engine) as session:
        session.add(patient)
        session.commit()
    return {"status": 200}

def select_all_patients():
    """Получение всех пациентов из БД"""
    with Session(engine) as session:
        statement = select(PatientTable)
        patients = session.exec(statement)
        patients_list = [patient.dict() for patient in patients]
    return patients_list
