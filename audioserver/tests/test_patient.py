import pytest
from pydantic import ValidationError
from models.models import Patient

patient_data = {
        'fullName': 'Иванов Иван Иванович',
        'dateOfBirth': '01.01.1990',
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
