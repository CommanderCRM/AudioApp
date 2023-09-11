from typing import Optional
from enum import Enum
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
                          json_schema_extra={
                          "example": "Иванов Иван Иванович",
                          "description": "Полное имя пациента"})
    dateOfBirth: str = Field(...,
                                  json_schema_extra={
                                  "example": "01.09.1990",
                                  "description": "Дата рождения пациента"})
    gender: Gender = Field(...,
                        json_schema_extra={
                        "example": "male",
                        "description": "Пол пациента"})
    medicalCardNumber: str = Field(...,
                                   json_schema_extra={
                                   "example": "11111111",
                                   "description": "Номер мед. карты пациента"})
    password: Optional[str] = Field(None,
                                    json_schema_extra={
                                    "example": None,
                                    "description": "Хэш постоянного пароля пациента"})
    temporaryPassword: Optional[str] = Field(None,
                                            json_schema_extra={
                                            "example": "c32041a07c88c1a1d429c12f3 etc",
                                            "description": "Хэш временного пароля пациента"})
    isPasswordChanged: bool = Field(...,
                                    json_schema_extra={
                                    "example": False,
                                    "description": "Флаг, указывающий, изменён ли пароль"})
    model_config = model_config
