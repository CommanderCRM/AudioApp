from enum import Enum
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from sqlalchemy import exc
from db.tables import PatientTable, ShortPatientModel
from db.actions import insert_patient, select_all_patients, select_patient_by_key, update_patient, delete_patient

app = FastAPI()

class ErrorCode(Enum):
    """Типы ошибок"""
    CARD_EXISTS = 1
    CONST_PASS_WITH_UNCHANGED_FLAG = 3
    TEMP_PASS_WITH_CHANGED_FLAG = 4

@app.post("/patients")
async def create_patient(patient: PatientTable):
    """Создание пациента по запросу POST"""
    if select_patient_by_key(patient.medical_card_number):
        return JSONResponse(content={"result_code": ErrorCode.CARD_EXISTS.value},
                            status_code=status.HTTP_400_BAD_REQUEST)

    if not patient.is_password_changed and patient.constant_password:
        return JSONResponse(content={"result_code": ErrorCode.CONST_PASS_WITH_UNCHANGED_FLAG.value},
                            status_code=status.HTTP_400_BAD_REQUEST)

    if patient.is_password_changed and patient.temporary_password:
        return JSONResponse(content={"result_code": ErrorCode.TEMP_PASS_WITH_CHANGED_FLAG.value},
                            status_code=status.HTTP_400_BAD_REQUEST)

    return insert_patient(patient)

@app.get("/patients")
async def get_patients():
    """Получение пациентов по запросу GET"""
    return select_all_patients()

@app.put("/patients/{medical_card_number}")
async def update_patient_record(medical_card_number: str, patient_update: ShortPatientModel):
    """Обновление информации o пациенте по запросу PUT"""
    try:
        return update_patient(medical_card_number, patient_update)
    except exc.IntegrityError:
        return JSONResponse(content={"result_code": ErrorCode.CARD_EXISTS.value},
                            status_code=status.HTTP_400_BAD_REQUEST)

@app.delete("/patients/{medical_card_number}")
async def delete_patient_record(medical_card_number: str):
    """Удаление информации o пациенте по запросу DELETE"""
    return delete_patient(medical_card_number)
