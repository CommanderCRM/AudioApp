from typing import Tuple, List
from sqlmodel import Session, create_engine, select
from .tables import PatientTable, DoctorTable, DoctorPatientTable, FullPatientModel

engine = create_engine("postgresql://postgres:postgres@sql:5432/postgres", echo=True)

def convert_full_model_to_table(full_patient_model: FullPatientModel) -> Tuple[PatientTable, List[DoctorPatientTable]]:
    """Перевод полной модели пациента в таблицу пациента
        Также заполнение таблицы доктор/пациент"""
    patient_table = PatientTable(
        card_number=full_patient_model.card_number,
        full_name=full_patient_model.full_name,
        gender=full_patient_model.gender,
        constant_password=full_patient_model.constant_password,
        hospital=full_patient_model.hospital,
        temporary_password=full_patient_model.temporary_password,
        is_password_changed=full_patient_model.is_password_changed,
        date_of_birth=full_patient_model.date_of_birth
    )
    doctor_patient_list = []
    for doctor in full_patient_model.doctor_info:
        doctor_patient = DoctorPatientTable(
            doctor_username=doctor,
            patient=patient_table
        )
        doctor_patient_list.append(doctor_patient)
    return patient_table, doctor_patient_list

def insert_patient(patient: PatientTable, doctor_patient_list: List[DoctorPatientTable]):
    """Запись пациента в БД"""
    with Session(engine) as session:
        session.add(patient)
        for doctor_patient in doctor_patient_list:
            session.add(doctor_patient)
        session.commit()
        session.refresh(patient)
        return

def insert_doctor(doctor: DoctorTable):
    """Запись пациента в БД"""
    with Session(engine) as session:
        session.add(doctor)
        session.commit()
        session.refresh(doctor)
        return

def select_all_patients():
    """Получение всех пациентов (короткая модель) из БД"""
    with Session(engine) as session:
        patients = session.query(PatientTable).with_entities(PatientTable.full_name,
                                                             PatientTable.date_of_birth,
                                                             PatientTable.gender,
                                                             PatientTable.card_number).all()
        return patients

def select_all_doctors():
    """Получение всех докторов из БД"""
    with Session(engine) as session:
        doctors = session.query(DoctorTable).all()
        return doctors

def select_patient_by_key(card_number: str):
    """Получение пациента по ключу"""
    with Session(engine) as session:
        patient = session.exec(select(PatientTable).where(PatientTable.card_number == card_number)).first()
        return bool(patient)
