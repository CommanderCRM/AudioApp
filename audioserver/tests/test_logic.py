from sqlmodel import create_engine, Session
from logic.actions import insert_patient
from logic.tables import PatientTable, DoctorPatientTable

def test_insert_patient():
    """Запись пациента в БД"""

    engine = create_engine('sqlite:///sqlite3.db')
    test_session = Session(engine)

    patient_table = PatientTable(
        card_number="111111111111",
        full_name="Test User",
        gender="M",
        constant_password="",
        hospital="TomskNII1",
        temporary_password="cbat",
        is_password_changed=0,
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
