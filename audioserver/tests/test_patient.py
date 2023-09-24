from datetime import date
import pytest
from pydantic import ValidationError
from db.tables import PostPatientInfo

patient_data = {
    'medical_card_number': '111',
    'full_name': 'Иван Иванович Иванов',
    'gender': 'm',
    'constant_password': '',
    'temporary_password': 'cbat',
    'is_password_changed': False,
    'date_of_birth': date(1990, 9, 1),
    'town': 'Tomsk'
    }

def test_correct_patient_data():
    """Корректные данные"""
    patient = PostPatientInfo(**patient_data)
    assert patient.dict() == patient_data # nosec

def test_incorrect_gender():
    """Неверный пол"""
    patient_data['gender'] = 'invalid_gender'
    with pytest.raises(ValidationError):
        PostPatientInfo(**patient_data)
