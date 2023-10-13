from typing import Tuple, List
import statistics
import os
from sqlmodel import Session, create_engine, select
from .tables import (PatientTable, DoctorPatientTable, PostPatientInfo, GetPatientInfo,
                     PostSessionInfo, SessionTable, PostSpeechInfo, SpeechTable,
                     SpeechSessionTable, GetSpeechInfoArray, GetSessionInfo,
                     GetSpeechInfo, GetSessionPatientInfo, SyllablesPhrasesTable,
                     GetPhrasesInfo, GetSessionInfoArray, SessionCompareTable,
                     SpeechCompareTable, SpeechCompares, SessionCompares,
                     PostSessionInfoReturn, PasswordStatus)
from .actionsaudio import compare_sessions_dtw, compare_phrases_levenstein
from .actionsauth import hash_gost_3411, validate_pass

if os.getenv('TESTING'):
    engine = create_engine('sqlite:///sqlite3.db')
else:
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

def convert_table_to_model(patient: PatientTable) -> GetPatientInfo:
    """Перевод таблицы пациента и таблицы доктор/пациент в короткую модель пациента"""
    with Session(engine) as session:
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
        if validate_pass(patient.temporary_password):
            patient.temporary_password = hash_gost_3411(patient.temporary_password)

        session.add(patient)
        session.commit()
        for doctor_patient in doctor_patient_list:
            session.add(doctor_patient)
        session.commit()
        session.refresh(patient)
        return

def select_all_patients(limit: int):
    """Получение всех пациентов из БД (короткая модель)"""
    with Session(engine) as session:
        patients = session.query(PatientTable).limit(limit).all()
        return [convert_table_to_model(patient) for patient in patients]

def select_patient_by_key(card_number: str):
    """Получение пациента по ключу"""
    with Session(engine) as session:
        patient = session.exec(select(PatientTable)
                               .where(PatientTable.card_number == card_number)).first()
        return bool(patient)

def insert_session_info(card_number: str, session_info: PostSessionInfo):
    """Запись информации o сессии в БД"""
    session_table = SessionTable(
        is_reference_session=session_info.is_reference_session,
        session_type=session_info.session_type,
        card_number=card_number
    )
    with Session(engine) as session:
        session.add(session_table)
        session.commit()
        session.refresh(session_table)
        return PostSessionInfoReturn(session_id=session_table.session_id)

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
        is_reference_speech=is_reference_speech,
        real_value=speech_info.real_value
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

def get_comparison_history(session: Session, comparison_table, session_id):
    """История сравнений сеансов"""
    comparison_history = session.exec(
        select(comparison_table)
        .where(comparison_table.compared_session_id_1 == session_id)
    ).all()

    # Сеансы, с которыми можем сравнивать - 2 или 3 (1 - референс)
    session_compares = []
    for compare in comparison_history:
        compared_sessions_ids = [
            getattr(compare, f'compared_session_id_{i}')
            for i in range(1, 4)
            if getattr(compare, f'compared_session_id_{i}', None) is not None
        ]
        session_compares.append(
                SessionCompares(
                    compared_sessions_id=compared_sessions_ids,
                    session_score=compare.session_score
                )
            )

    return session_compares

def select_session_info(_, session_id):
    """Получение информации o сеансе и записях речи в нем"""
    with Session(engine) as session:
        session_info = session.exec(select(SessionTable)
                                    .where(SessionTable.session_id == session_id)).first()
        speech_session_info = session.exec(select(SpeechSessionTable.speech_id)
                                           .where(SpeechSessionTable.session_id == session_id)).all()
        session_compares = get_comparison_history(session, SessionCompareTable, session_id)

        # В каждом сеансе может быть несколько записей речи, заполняем информацию о каждой
        speech_array = []
        for speech_id in speech_session_info:
            speech_info = session.exec(select(SpeechTable)
                                       .where(SpeechTable.speech_id == speech_id)).first()
            speech_compares = session.exec(select(SpeechCompareTable)
                                           .where(SpeechCompareTable.compared_speech_id_1 == speech_id)).all()

            # Также каждая запись могла сравниваться с несколькими другими записями, заполнение истории сравнений
            # Речи, с которыми можем сравнивать - 2 или 3 (1 - референс)
            speech_compares_history = []
            for compare in speech_compares:
                compared_speech_ids = [
                    getattr(compare, f'compared_speech_id_{i}')
                    for i in range(1, 4)
                    if getattr(compare, f'compared_speech_id_{i}', None) is not None
                    ]

                for compared_speech_id in compared_speech_ids:
                    compared_session_id = session.exec(
                        select(SpeechSessionTable.session_id)
                        .where(SpeechSessionTable.speech_id == compared_speech_id)
                        ).first()
                    speech_score = compare.speech_score

                    speech_compares_history.append(SpeechCompares(compared_session_id=compared_session_id,
                                                              compared_speech_id=[compared_speech_id],
                                                              speech_score=speech_score))

            speech_array.append(GetSpeechInfoArray(speech_id=speech_info.speech_id,
                                                   speech_compares_history=speech_compares_history,
                                                   speech_type=speech_info.speech_type,
                                                   is_reference_speech=speech_info.is_reference_speech,
                                                   real_value=speech_info.real_value))

        return GetSessionInfo(is_reference_session=session_info.is_reference_session,
                              session_type=session_info.session_type,
                              speech_array=speech_array,
                              session_compares=session_compares)

def select_session_patient_info(session_id):
    """Получение информации o сеансе для пациента"""
    with Session(engine) as session:
        session_info = session.exec(select(SessionTable)
                                    .where(SessionTable.session_id == session_id)).first()

        session_compares_history = get_comparison_history(session, SessionCompareTable, session_id)

        return GetSessionInfoArray(session_id=session_info.session_id,
                                   session_compares_history=session_compares_history,
                                   is_reference_session=session_info.is_reference_session,
                                   session_type=session_info.session_type)

def select_session_by_key(session_number: int):
    """Получение сеанса по ключу"""
    with Session(engine) as db_session:
        session = db_session.exec(select(SessionTable)
                                  .where(SessionTable.session_id == session_number)).first()
        return bool(session)

def select_speech_info(_, __, speech_id):
    """Получение информации o речи"""
    with Session(engine) as session:
        speech_info = session.exec(select(SpeechTable)
                                   .where(SpeechTable.speech_id == speech_id)).first()
        speech_value = speech_info.base64_value
        return GetSpeechInfo(base64_value=speech_value)

def select_patient_and_sessions(card_number: str):
    """Получение информации o пациенте и ero сеансах"""
    with Session(engine) as session:
        patient = session.exec(select(PatientTable)
                               .where(PatientTable.card_number == card_number)).first()
        patient_info = convert_table_to_model(patient)

        patient_sessions = session.exec(select(SessionTable)
                                        .where(SessionTable.card_number == card_number)).all()
        session_info_list = [select_session_patient_info(session.session_id)
                             for session in patient_sessions]

        return GetSessionPatientInfo(get_patient_info=patient_info, sessions=session_info_list)

def select_phrases_and_syllables():
    """Получение информации o фразах и слогах"""
    with Session(engine) as session:
        phrases_query = select(SyllablesPhrasesTable).where(SyllablesPhrasesTable.syllable_phrase_type == "phrase")
        syllables_query = select(SyllablesPhrasesTable).where(SyllablesPhrasesTable.syllable_phrase_type == "syllable")

        phrases_results = session.execute(phrases_query).fetchall()
        syllables_results = session.execute(syllables_query).fetchall()

        phrases_list = [result[0].value for result in phrases_results]
        syllables_list = [result[0].value for result in syllables_results]

        return GetPhrasesInfo(phrases=phrases_list, syllables=syllables_list)

def get_session_speech_array(session_id: int):
    """Получение всех записей речи в сеансе"""
    with Session(engine) as session:
        speech_session_info = session.exec(select(SpeechSessionTable.speech_id)
                                           .where(SpeechSessionTable.session_id == session_id)).all()

        speech_array = []
        for speech_id in speech_session_info:
            speech_info = session.exec(select(SpeechTable)
                                       .where(SpeechTable.speech_id == speech_id)).first()
            speech_array.append(GetSpeechInfoArray(**speech_info.__dict__))

        return speech_array

def get_speech_value(speech_id: int):
    """Получение base64-значения речи по ee ID"""
    with Session(engine) as session:
        speech_info = session.exec(select(SpeechTable)
                                   .where(SpeechTable.speech_id == speech_id)).first()
        return speech_info.base64_value

def compare_two_sessions(_, session_1_id: int, session_2_id: int):
    """Сравнение двух сеансов"""
    session_1_speeches = get_session_speech_array(session_1_id)
    session_2_speeches = get_session_speech_array(session_2_id)

    comparable_speech_ids = {}
    comparable_key = 0

    # Получение тех записей речи, которые можно сравнить
    for speech_1 in session_1_speeches:
        for speech_2 in session_2_speeches:
            if speech_1.speech_type == speech_2.speech_type and speech_1.real_value == speech_2.real_value:
                comparable_speech_ids[comparable_key] = [speech_1.speech_id, speech_2.speech_id]
                comparable_key += 1

    speech_values_dict = {}
    speech_value_key = 0

    # Получение base64 значений сравниваемых записей речи
    for comparable_key, speech_ids in comparable_speech_ids.items():
        speech_1_value = get_speech_value(speech_ids[0])
        speech_2_value = get_speech_value(speech_ids[1])
        speech_values_dict[speech_value_key] = [speech_1_value, speech_2_value]
        speech_value_key += 1

    # Получение расстояний DTW для каждой пары слогов и общей оценки сеанса (среднее)
    dtw_distances = compare_sessions_dtw(speech_values_dict)
    dtw_mean = statistics.mean(dtw_distances.values())

    # Заполнение таблицы сравнения сеансов
    with Session(engine) as session:
        session_compare = SessionCompareTable(
            compared_session_id_1=session_1_id,
            compared_session_id_2=session_2_id,
            session_score=dtw_mean,
        )
        session.add(session_compare)
        session.commit()

    # Заполнение таблицы сравнения записей речи
    with Session(engine) as session:
        for key, value in comparable_speech_ids.items():
            speech_compare = SpeechCompareTable(
                compared_speech_id_1=value[0],
                compared_speech_id_2=value[1],
                speech_score=dtw_distances[key],
            )
            session.add(speech_compare)
            session.commit()

def compare_phrases_real(_, session_id: int):
    """Сравнение фраз с реальным значением"""
    SPEECH_TYPE = 'фраза'

    phrases_info = {}

    # Заполнение инф. о фразе (ID, эталон, base64)
    session_speeches = get_session_speech_array(session_id)
    for speech_data in session_speeches:
        if speech_data.speech_type == SPEECH_TYPE:
            phrase_base64 = get_speech_value(speech_data.speech_id)
            phrases_info[speech_data.speech_id] = [speech_data.real_value, phrase_base64]

    phrases_scores = {}
    # Получение точности сравнения с эталоном
    for key, value in phrases_info.items():
        score = compare_phrases_levenstein(value[0], value[1])
        phrases_scores[key] = score

    # Общая оценка сеанса
    accuracy_mean = statistics.mean(phrases_scores[i] for i in phrases_scores)

    # Заполнение таблицы сравнения сеансов
    with Session(engine) as session:
        session_compare = SessionCompareTable(
            compared_session_id_1=session_id,
            session_score=accuracy_mean,
        )
        print(session_compare)
        session.add(session_compare)
        session.commit()

    # Заполнение таблицы сравнения записей речи
    with Session(engine) as session:
        for key, value in phrases_scores.items():
            speech_compare = SpeechCompareTable(
                compared_speech_id_1=key,
                speech_score=value,
            )
            print(speech_compare)
            session.add(speech_compare)
            session.commit()

def select_password_status(card_number: str):
    """Получение информации о статусе пароля"""
    with Session(engine) as session:
        patient = session.exec(select(PatientTable)
                               .where(PatientTable.card_number == card_number)).first()
        return PasswordStatus(is_password_changed=patient.is_password_changed)
