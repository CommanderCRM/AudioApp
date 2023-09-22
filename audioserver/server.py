from enum import Enum
from fastapi import FastAPI, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from db.tables import DoctorTable, FullPatientModel
from db.actions import insert_patient, select_all_patients, select_patient_by_key, insert_doctor, select_all_doctors, convert_full_model_to_table

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
async def create_patient(patient: FullPatientModel):
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

@app.post("/doctors")
async def create_doctor(doctor: DoctorTable):
    """Создание доктора по запросу POST"""
    return insert_doctor(doctor)

@app.get("/doctors")
async def get_doctors():
    """Получение докторов по запросу GET"""
    return select_all_doctors()

@app.get("/patients")
async def get_patients():
    """Получение пациентов по запросу GET"""
    return select_all_patients()

@app.post("/patients/{card_number}/speech")
async def upload_record_speech(_, __):
    """Загрузить/записать речь"""
    return
