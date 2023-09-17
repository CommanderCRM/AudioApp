from enum import Enum
from fastapi import FastAPI, Response, status
from db.tables import PatientTable
from db.actions import insert_patient, select_all_patients, select_patient_by_key

app = FastAPI()

class ErrorCode(Enum):
    """Типы ошибок"""
    CARD_EXISTS = 1
    CONST_PASS_WITH_UNCHANGED_FLAG = 3
    TEMP_PASS_WITH_CHANGED_FLAG = 4

@app.post("/patients")
async def create_patient(patient: PatientTable, response: Response):
    """Создание пациента по запросу POST"""
    if select_patient_by_key(patient.medicalcardnumber):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorCode.CARD_EXISTS

    if not patient.ispasswordchanged and patient.constantpassword:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorCode.CONST_PASS_WITH_UNCHANGED_FLAG

    if patient.ispasswordchanged and patient.temporarypassword:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorCode.TEMP_PASS_WITH_CHANGED_FLAG

    return insert_patient(patient)

@app.get("/patients")
async def get_patients():
    """Получение пациентов по запросу GET"""
    return select_all_patients()
