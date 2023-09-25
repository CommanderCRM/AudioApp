from typing import Tuple, List
from sqlmodel import Session, create_engine, select
from .tables import PatientTable, DoctorPatientTable, PostPatientInfo, GetPatientInfo, PostSessionInfo, SessionTable, PostSpeechInfo, SpeechTable, SpeechSessionTable

engine = create_engine("postgresql://postgres:postgres@sql:5432/postgres", echo=True)

def convert_full_model_to_table(full_patient_model: PostPatientInfo) -> Tuple[PatientTable, List[DoctorPatientTable]]:
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
            patient_card_number=patient_table.card_number
        )
        doctor_patient_list.append(doctor_patient)
    return patient_table, doctor_patient_list

def convert_table_to_model(patient: PatientTable, session: Session) -> GetPatientInfo:
    """Перевод таблицы пациента и таблицы доктор/пациент в короткую модель пациента"""
    doctor_patient_records = session.query(DoctorPatientTable).filter_by(patient_card_number = patient.card_number).all()
    doctor_info = [record.doctor_username for record in doctor_patient_records]
    return GetPatientInfo(
        full_name=patient.full_name,
        date_of_birth=patient.date_of_birth,
        gender=patient.gender,
        card_number=patient.card_number,
        doctor_info=doctor_info
    )

def insert_patient(patient: PatientTable, doctor_patient_list: List[DoctorPatientTable]):
    """Запись пациента в БД"""
    with Session(engine) as session:
        session.add(patient)
        session.commit()
        for doctor_patient in doctor_patient_list:
            session.add(doctor_patient)
        session.commit()
        session.refresh(patient)
        return

def select_all_patients():
    """Получение всех пациентов из БД (короткая модель)"""
    with Session(engine) as session:
        patients = session.query(PatientTable).all()
        return [convert_table_to_model(patient, session) for patient in patients]

def select_patient_by_key(card_number: str):
    """Получение пациента по ключу"""
    with Session(engine) as session:
        patient = session.exec(select(PatientTable).where(PatientTable.card_number == card_number)).first()
        return bool(patient)

def insert_session_info(card_number: str, session_info: PostSessionInfo):
    """Запись информации o сессии в БД"""
    session_table = SessionTable(
        is_reference_session=session_info.is_reference_session,
        card_number=card_number
    )
    with Session(engine) as session:
        session.add(session_table)
        session.commit()
        session.refresh(session_table)
        return

def insert_speech(_, session_id: int, speech_info: PostSpeechInfo):
    """Запись речи в БД"""
    with Session(engine) as session:
        session_record = session.query(SessionTable).filter(SessionTable.session_id == session_id).first()
        if session_record is not None:
            is_reference_speech = session_record.is_reference_session

    speech_table = SpeechTable(
        speech_type=speech_info.speech_type,
        base64_value=speech_info.base64_value,
        base64_segment_value=speech_info.base64_value_segment,
        is_reference_speech=is_reference_speech
    )
    with Session(engine) as session:
        session.add(speech_table)
        session.commit()
        speech_session_table = SpeechSessionTable(
            speech_id=speech_table.speech_id,
            session_id=session_id
        )
        session.add(speech_session_table)
        session.commit()
