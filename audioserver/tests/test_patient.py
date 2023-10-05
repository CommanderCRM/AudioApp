from datetime import date
import pytest
from pydantic import ValidationError
from logic.tables import PostPatientInfo

patient_data = {
    "full_name": "Иванов Иван Иванович",
    "date_of_birth": date(1990, 7, 7),
    "doctor_info": [
        "user1", "user2"
    ],
    "hospital": "Tomsk NII",
    "gender": "m",
    "card_number": "111111111111",
    "constant_password": "",
    "temporary_password": "c32041a07c88c1a1d429c12f35e26c5f44e7e85e2f7a37eb157dd34f3290e5e2",
    "is_password_changed": False
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
