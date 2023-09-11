from typing import Optional
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field

class Gender(str, Enum):
    """Массив пола"""
    male = "male"
    female = "female"

model_config = {
    'use_enum_values': True
}

class Patient(BaseModel):
    """Схема данных пациента"""
    fullName: str = Field(...,
                          example="Иванов Иван Иванович",
                          description="Полное имя пациента")
    dateOfBirth: datetime = Field(...,
                                  example="01.09.1990",
                                  description="Дата рождения пациента")
    gender: Gender = Field(...,
                        example="male",
                        description="Пол пациента")
    medicalCardNumber: str = Field(...,
                                   example="11111111",
                                   description="Номер мед. карты пациента")
    password: Optional[str] = Field(None,
                                    example=None,
                                    description="Хэш постоянного пароля пациента")
    temporaryPassword: Optional[str] = Field(None,
                                            example="c32041a07c88c1a1d429c12f3 etc",
                                            description="Хэш временного пароля пациента")
    isPasswordChanged: bool = Field(...,
                                    example=False,
                                    description="Флаг, указывающий, изменён ли пароль")
    model_config = model_config
