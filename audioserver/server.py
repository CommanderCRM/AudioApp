from enum import Enum
from fastapi import FastAPI, status, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from logic.tables import PostPatientInfo, PostSessionInfo, PostSpeechInfo, CompareSessionsIDs
from logic.actions import (insert_patient, select_all_patients, select_patient_by_key,
                        convert_full_model_to_table, insert_session_info, insert_speech,
                        select_session_info, select_speech_info, select_session_by_key,
                        select_patient_and_sessions, select_phrases_and_syllables,
                        compare_two_sessions)

app = FastAPI()

class ErrorCode(Enum):
    """Типы ошибок"""
    CARD_EXISTS = 1
    CONST_PASS_WITH_UNCHANGED_FLAG = 3
    TEMP_PASS_WITH_CHANGED_FLAG = 4
    INTERNAL_SERVER_ERROR = 5
    API_VALIDATION_ERROR = 6

@app.exception_handler(HTTPException)
async def internal_server_error_handler(_, exception: HTTPException):
    """Обработка внутренней ошибки сервера 500"""
    if exception.status_code == 500:
        return JSONResponse(content={"result_code": ErrorCode.INTERNAL_SERVER_ERROR.value},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # Все остальное уходит в обычную обработку ошибок
    return await app.exception_handler(exception)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, __):
    """Обработка ошибки валидации данных"""
    return JSONResponse(content={"result_code": ErrorCode.API_VALIDATION_ERROR.value},
                            status_code=status.HTTP_400_BAD_REQUEST)

@app.post("/patients")
async def create_patient(patient: PostPatientInfo):
    """Создание пациента по запросу POST"""
    patient_table, doctor_patient_list = convert_full_model_to_table(patient)

    if select_patient_by_key(patient_table.card_number):
        return JSONResponse(content={"result_code": ErrorCode.CARD_EXISTS.value},
                            status_code=status.HTTP_400_BAD_REQUEST)

    if not patient_table.is_password_changed and patient_table.constant_password:
        return JSONResponse(content={"result_code": ErrorCode.CONST_PASS_WITH_UNCHANGED_FLAG.value},
                            status_code=status.HTTP_400_BAD_REQUEST)

    if patient_table.is_password_changed and patient_table.temporary_password:
        return JSONResponse(content={"result_code": ErrorCode.TEMP_PASS_WITH_CHANGED_FLAG.value},
                            status_code=status.HTTP_400_BAD_REQUEST)

    return insert_patient(patient_table, doctor_patient_list)

@app.get("/patients")
async def get_patients(limit: int):
    """Получение пациентов по запросу GET"""
    return select_all_patients(limit)

@app.post("/patients/{card_number}")
async def post_session_info(card_number: str, session_info: PostSessionInfo):
    """Добавить информацию o сеансе"""
    if not select_patient_by_key(card_number):
        raise HTTPException(status_code=404)

    return insert_session_info(card_number, session_info)

@app.post("/patients/{card_number}/speech/{session_id}")
async def upload_record_speech(card_number: str, session_id: int, speech_info: PostSpeechInfo):
    """Загрузить/записать речь в сеанс"""
    if not select_patient_by_key(card_number):
        raise HTTPException(status_code=404)

    return insert_speech(card_number, session_id, speech_info)

@app.get("/patients/{card_number}/session/{session_id}")
async def get_session_info(card_number: str, session_id: int):
    """Получить информацию o сессии"""

    return select_session_info(card_number, session_id)

@app.get("/patients/{card_number}/session/{session_id}/speech/{speech_id}")
async def get_speech_info(card_number: str, session_id: int, speech_id: int):
    """Получить информацию o речи"""
    if not select_patient_by_key(card_number) or not select_session_by_key(session_id):
        raise HTTPException(status_code=404)

    return select_speech_info(card_number, session_id, speech_id)

@app.get("/patients/{card_number}")
async def get_patient_and_sessions(card_number: str):
    """Получить информацию o пациенте и ero сеансах"""

    return select_patient_and_sessions(card_number)

@app.get("/patients/{card_number}/session/{session_id}/speech")
async def get_phrases_and_syllables_info():
    """Получить информацию o фразах и слогах"""

    return select_phrases_and_syllables()

@app.patch("/patients/{card_number}/session")
async def compare_sessions(card_number: int, request: Request):
    """Сравнение сеансов (аудиофайлы)"""
    data = await request.json()
    session_ids = CompareSessionsIDs(**data)

    session_1_id = session_ids.sessions_id[0]
    session_2_id = session_ids.sessions_id[1]

    if not select_session_by_key(session_1_id) or not select_session_by_key(session_2_id):
        raise HTTPException(status_code=404)

    return compare_two_sessions(card_number, session_1_id, session_2_id)
