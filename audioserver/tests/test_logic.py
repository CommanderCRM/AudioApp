import os
import sys
from sqlmodel import create_engine, Session
from logic.actions import insert_patient, select_all_patients, select_patient_by_key
from logic.tables import PatientTable, DoctorPatientTable

if not os.getenv('TESTING'):
    print('Установите переменную среды TESTING!')
    sys.exit(1)

def test_insert_patient():
    """Запись пациента в БД"""

    engine = create_engine('sqlite:///sqlite3.db')
    test_session = Session(engine)

    patient_table = PatientTable(
        card_number="111111111111",
        full_name="Test User",
        gender="M",
        constant_password="", # nosec
        hospital="TomskNII1",
        temporary_password="cbat", # nosec
        is_password_changed=0, # nosec
        date_of_birth="2000-01-01"
    )
    doctor_patient_table = DoctorPatientTable(
        doctor_patient_id=1,
        doctor_username="user1",
        patient_card_number="111111111111"
    )

    insert_patient(patient_table, [doctor_patient_table])

    patient_in_db = test_session.get(PatientTable, patient_table.card_number)
    assert patient_in_db is not None # nosec

def test_select_all_patients():
    """Получение всех пациентов из БД (короткая модель)"""

    for i in range(2,4):
        patient_table = PatientTable(
            card_number=f"11111111111{i}",
            full_name=f"Test User {i}",
            gender="M",
            constant_password="", # nosec
            hospital="TomskNII1",
            temporary_password="cbat", # nosec
            is_password_changed=0, # nosec
            date_of_birth="2000-01-01"
        )
        doctor_patient_table = DoctorPatientTable(
            doctor_patient_id={i},
            doctor_username=f"user{i}",
            patient_card_number=f"11111111111{i}"
        )
        insert_patient(patient_table, [doctor_patient_table])

    patients = select_all_patients(2)
    assert len(patients) == 2 # nosec

def test_select_patient_by_key():
    """Получение пациента по ключу"""

    patient_table = PatientTable(
        card_number="111111111114",
        full_name="Test User 4",
        gender="M",
        constant_password="", # nosec
        hospital="TomskNII1",
        temporary_password="cbat", # nosec
        is_password_changed=0, # nosec
        date_of_birth="2000-01-01"
    )
    doctor_patient_table = DoctorPatientTable(
            doctor_patient_id=4,
            doctor_username="user4",
            patient_card_number="111111111114"
    )
    insert_patient(patient_table, [doctor_patient_table])

    assert select_patient_by_key("111111111114") # nosec
    assert not select_patient_by_key("nonexistent_card_number") # nosec
