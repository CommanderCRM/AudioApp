from enum import Enum
from datetime import date
from typing import Optional
from sqlmodel import Field, SQLModel

class Gender(str, Enum):
    """Массив пола"""
    male = "m"
    female = "f"

class Patient(SQLModel):
    '''Модель пациента'''
    medicalcardnumber: str = Field(
        default=None,
        title="111",
        description="Номер мед. карты",
        max_length=12
    )
    fullname: str = Field(
        title="Иван Иванович Иванов",
        description="Полное имя пациента",
        max_length=255
    )
    gender: Gender = Field(
        title="m",
        description="Пол пациента",
        max_length=1
    )
    constantpassword: Optional[str] = Field(
        default=None,
        title=None,
        description="Хэш постоянного пароля пациента",
        max_length=128
    )
    temporarypassword: Optional[str] = Field(
        default=None,
        title="c32041a07c88c1a1d429c12f3 etc",
        description="Хэш временного пароля пациента",
        max_length=128
    )
    ispasswordchanged: bool = Field(
        title=False,
        description="Флаг, указывающий, изменён ли пароль"
    )
    dateofbirth: date = Field(
        title="1990-09-01",
        description="Дата рождения пациента"
    )

    class Config():
        """Конфигурация модели"""
        use_enum_values = True

class PatientTable(Patient, table=True):
    '''Таблица пациента SQL'''
    medicalcardnumber: str = Field(
        default=None,
        primary_key=True,
        title="111",
        description="Номер мед. карты",
        max_length=12,
    )
