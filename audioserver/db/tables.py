from enum import Enum
from datetime import date
from typing import Optional
from sqlmodel import Field, SQLModel

class Gender(str, Enum):
    """Массив пола"""
    male = "m"
    female = "f"

class PatientTable(SQLModel, table=True):
    '''Таблица пациента'''
    __tablename__: str = "patient_table"
    medical_card_number: str = Field(
        default=None,
        primary_key=True,
        title="111",
        description="Номер мед. карты",
        max_length=12
    )
    full_name: str = Field(
        title="Иван Иванович Иванов",
        description="Полное имя пациента",
        max_length=255
    )
    gender: Gender = Field(
        title="m",
        description="Пол пациента",
        max_length=1
    )
    constant_password: Optional[str] = Field(
        default=None,
        title=None,
        description="Хэш постоянного пароля пациента",
        max_length=128
    )
    temporary_password: Optional[str] = Field(
        default=None,
        title="c32041a07c88c1a1d429c12f3 etc",
        description="Хэш временного пароля пациента",
        max_length=128
    )
    is_password_changed: bool = Field(
        title=False,
        description="Флаг, указывающий, изменён ли пароль"
    )
    date_of_birth: date = Field(
        title="1990-09-01",
        description="Дата рождения пациента"
    )
    town: str = Field(
        title="Tomsk",
        description="Город пациента",
        max_length=64
    )

    class Config():
        """Конфигурация модели"""
        use_enum_values = True

class FullPatientModel(SQLModel):
    '''Полная модель пациента'''
    medical_card_number: str = Field(
        default=None,
        title="111",
        description="Номер мед. карты",
        max_length=12
    )
    full_name: str = Field(
        title="Иван Иванович Иванов",
        description="Полное имя пациента",
        max_length=255
    )
    gender: Gender = Field(
        title="m",
        description="Пол пациента",
        max_length=1
    )
    constant_password: Optional[str] = Field(
        default=None,
        title=None,
        description="Хэш постоянного пароля пациента",
        max_length=128
    )
    temporary_password: Optional[str] = Field(
        default=None,
        title="c32041a07c88c1a1d429c12f3 etc",
        description="Хэш временного пароля пациента",
        max_length=128
    )
    is_password_changed: bool = Field(
        title=False,
        description="Флаг, указывающий, изменён ли пароль"
    )
    date_of_birth: date = Field(
        title="1990-09-01",
        description="Дата рождения пациента"
    )
    town: str = Field(
        title="Tomsk",
        description="Город пациента",
        max_length=64
    )

    class Config():
        """Конфигурация модели"""
        use_enum_values = True

class ShortPatientModel(SQLModel):
    '''Короткая модель пациента'''
    full_name: str = Field(
        title="Иван Иванович Иванов",
        description="Полное имя пациента",
        max_length=255
    )
    medical_card_number: str = Field(
        default=None,
        title="111",
        description="Номер мед. карты",
        max_length=12
    )
    gender: Gender = Field(
        title="m",
        description="Пол пациента",
        max_length=1
    )
    date_of_birth: date = Field(
        title="1990-09-01",
        description="Дата рождения пациента"
    )

    class Config():
        """Конфигурация модели"""
        use_enum_values = True
