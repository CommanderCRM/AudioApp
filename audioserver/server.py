from fastapi import FastAPI
from db.tables import PatientTable
from db.actions import insert_patient, select_all_patients

app = FastAPI()

@app.post("/patients")
async def create_patient(patient: PatientTable):
    """Создание пациента по запросу POST"""
    return insert_patient(patient)

@app.get("/patients")
async def get_patients():
    """Получение пациентов по запросу GET"""
    return select_all_patients()
