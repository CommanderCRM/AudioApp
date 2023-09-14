from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field

class Gender(str, Enum):
    """Массив пола"""
    male = "male"
    female = "female"
class Patient(BaseModel):
    """Схема данных пациента"""
    fullName: str = Field(...,
                          title="Иванов Иван Иванович",
                          description="Полное имя пациента")
    dateOfBirth: str = Field(...,
                             title="01.09.1990",
                             description="Дата рождения пациента")
    gender: Gender = Field(...,
                           title="male",
                           description="Пол пациента")
    medicalCardNumber: str = Field(...,
                                   title="11111111",
                                   description="Номер мед. карты пациента")
    password: Optional[str] = Field(None,
                                    title=None,
                                    description="Хэш постоянного пароля пациента")
    temporaryPassword: Optional[str] = Field(None,
                                            title="c32041a07c88c1a1d429c12f3 etc",
                                            description="Хэш временного пароля пациента")
    isPasswordChanged: bool = Field(...,
                                    title=False,
                                    description="Флаг, указывающий, изменён ли пароль")
    class Config:
        """Конфигурация модели"""
        use_enum_values = True
