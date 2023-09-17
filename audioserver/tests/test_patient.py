from datetime import date
import pytest
from pydantic import ValidationError
from db.tables import Patient

patient_data = {
    'medicalcardnumber': '111',
    'fullname': 'Иван Иванович Иванов',
    'gender': 'm',
    'constantpassword': '',
    'temporarypassword': 'cbat',
    'ispasswordchanged': False,
    'dateofbirth': date(1990, 9, 1)
    }

def test_correct_patient_data():
    """Корректные данные"""
    patient = Patient(**patient_data)
    assert patient.dict() == patient_data

def test_incorrect_gender():
    """Неверный пол"""
    patient_data['gender'] = 'invalid_gender'
    with pytest.raises(ValidationError):
        Patient(**patient_data)
