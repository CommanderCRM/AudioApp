from fastapi import FastAPI
from models.models import Patient

app = FastAPI()

@app.post("/patients")
async def create_patient(patient: Patient):
    """Создание пациента по запросу POST"""
    return patient
