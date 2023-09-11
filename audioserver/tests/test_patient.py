from datetime import datetime
import pytest
from pydantic import ValidationError
from models.models import Patient

patient_data = {
        'fullName': 'Иванов Иван Иванович',
        'dateOfBirth': datetime(1990, 9, 1),
        'gender': 'male',
        'medicalCardNumber': '11111111',
        'isPasswordChanged': False,
        'password': None,
        'temporaryPassword': 'cbat'
    }

def test_correct_patient_data():
    """Корректные данные"""
    patient = Patient(**patient_data)
    assert patient.model_dump() == patient_data

def test_incorrect_gender():
    """Неверный пол"""
    patient_data['gender'] = 'invalid_gender'
    with pytest.raises(ValidationError):
        Patient(**patient_data)

def test_incorrect_date():
    """Неверная дата"""
    patient_data['dateOfBirth'] = 'incorrect_date'
    with pytest.raises(ValidationError):
        Patient(**patient_data)
