from enum import Enum
from datetime import date
from typing import Optional, List
from sqlmodel import Field, SQLModel, Column, String

class Gender(str, Enum):
    """Массив пола"""
    MALE = "m"
    FEMALE = "f"

class Hospital(str, Enum):
    """Массив больниц"""
    HOSP_TOMSK = "Tomsk NII"
    HOSP_MSK_FIRST = "Moscow NII_1"
    HOSP_MSK_SECOND = "Moscow NII_2"

class SpeechType(str, Enum):
    """Массив типов речи"""
    PHRASE = "фраза"
    SYLLABLE = "слог"

class SessionType(str, Enum):
    """Массив типов сессии"""
    PHRASES = "фразы"
    SYLLABLES = "слоги"

class PatientTable(SQLModel, table=True):
    """Таблица пациента"""
    __tablename__: str = "patient_table"
    card_number: str = Field(
        default=None,
        primary_key=True,
        title="111111111111",
        description="Номер карты",
        min_length=12,
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
    hospital: Hospital = Field(
        default=None,
        title="Tomsk NII",
        description="Больница",
        max_length=64
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
    class Config():
        """Конфигурация модели"""
        use_enum_values = True

class PostPatientInfo(SQLModel):
    """Полная модель пациента"""
    full_name: str = Field(
        title="Иван Иванович Иванов",
        description="Полное имя пациента",
        max_length=255
    )
    date_of_birth: date = Field(
        title="1990-09-01",
        description="Дата рождения пациента"
    )
    doctor_info: List[str] = Field(
        title="boralek, shabanov",
        description="Идентификаторы лечащих врачей"
    )
    hospital: Hospital = Field(
        title="Tomsk NII",
        description="Больница",
        max_length=64
    )
    gender: Gender = Field(
        title="m",
        description="Пол пациента",
        max_length=1
    )
    card_number: str = Field(
        default=None,
        primary_key=True,
        title="111111111111",
        description="Номер карты",
        min_length=12,
        max_length=12
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
    class Config():
        """Конфигурация модели"""
        use_enum_values = True

class GetPatientInfo(SQLModel):
    """Короткая модель пациента"""
    full_name: str = Field(
        title="Иван Иванович Иванов",
        description="Полное имя пациента",
        max_length=255
    )
    date_of_birth: date = Field(
        title="1990-09-01",
        description="Дата рождения пациента"
    )
    gender: Gender = Field(
        title="m",
        description="Пол пациента",
        max_length=1
    )
    card_number: str = Field(
        default=None,
        title="111",
        description="Номер мед. карты",
        min_length=12,
        max_length=12
    )
    doctor_info: List[str] = Field(
        title="boralek, shabanov",
        description="Идентификаторы лечащих врачей"
    )
    class Config():
        """Конфигурация модели"""
        use_enum_values = True

class DoctorTable(SQLModel, table=True):
    """Таблица врача"""
    __tablename__: str = "doctor_table"
    username: str = Field(
        default=None,
        primary_key=True,
        title="boralek",
        description="Имя пользователя врача",
        max_length=255
    )
    specialization: str = Field(
        title="логопед",
        description="Специализация врача",
        max_length=255
    )
    hospital: Hospital = Field(
        title="Tomsk NII",
        description="Больница",
        max_length=64
    )
    password: str = Field(
        default=None,
        title="c32041a07c88c1a1d429c12f3",
        description="Хэш постоянного пароля врача",
        max_length=128
    )
    full_name: str = Field(
        title="Алексей Алексеевич Боровской",
        description="Полное имя врача",
        max_length=255
    )

class PostSpeechInfo(SQLModel):
    """Модель информации o речи"""
    speech_type: SpeechType = Field(
        title="слог",
        description="Биологический тип сигнала"
    )
    base64_value: str = Field(
        title="UklGRgYvAABXQVZFZm",
        description="Записанный звуковой файл, закодированный в base64"
    )
    base64_value_segment: Optional[str] = Field(
        title="UklGRgYvAABXQVZFZm",
        description="Сегментированное значение речи, закодированное в base64"
    )
    real_value: str = Field(
        title="кась",
        description="Реальное значение слога или фразы, которое должно было быть произнесено"
    )

class DoctorPatientTable(SQLModel, table=True):
    """Связь доктора/пациента"""
    __tablename__: str = "doctor_patient_table"
    doctor_patient_id: Optional[int] = Field(default=None, primary_key=True)
    doctor_username: str = Field(foreign_key="doctor_table.username")
    patient_card_number: str = Field(foreign_key="patient_table.card_number")

class PostSessionInfo(SQLModel):
    """Информация o сессии POST"""
    is_reference_session: bool = Field(
        title="true",
        description="Флаг, указывающий на то, является ли сеанс эталонным"
    )
    session_type: SessionType = Field(
        title="фразы",
        description="Тип биологического сигнала, записываемый в рамках одного сеанса"
    )

class SessionTable(SQLModel, table=True):
    """Таблица сессии"""
    __tablename__: str = "session_table"
    session_id: Optional[int] = Field(default=None, primary_key=True)
    is_reference_session: bool = Field(
        title="true",
        description="Флаг, указывающий на то, является ли сеанс эталонным"
    )
    session_type: SessionType = Field(
        title="фразы",
        description="Тип биологического сигнала, записываемый в рамках одного сеанса"
    )
    card_number: str = Field(foreign_key="patient_table.card_number")

class SpeechTable(SQLModel, table=True):
    """Таблица информации o речи"""
    __tablename__: str = "speech_table"
    speech_id: Optional[int] = Field(default=None, primary_key=True)
    speech_type: SpeechType = Field(
        title="слог",
        description="Биологический тип сигнала"
    )
    base64_value: str = Field(
        title="UklGRgYvAABXQVZFZm",
        description="Записанный звуковой файл, закодированный в base64"
    )
    base64_segment_value: Optional[str] = Field(
        title="UklGRgYvAABXQVZFZm",
        description="Сегментированное значение речи, закодированное в base64"
    )
    is_reference_speech: bool = Field(
        title="true",
        description="Флаг, указывающий на то, является ли речь эталонной"
    )
    real_value: str = Field(
        title="кась",
        description="Реальное значение слога или фразы, которое должно было быть произнесено"
    )

class SpeechSessionTable(SQLModel, table=True):
    """Таблица отношения речь/сеанс"""
    __tablename__: str = "speech_session_table"
    speech_session_id: Optional[int] = Field(default=None, primary_key=True)
    speech_id: int = Field(foreign_key="speech_table.speech_id")
    session_id: int = Field(foreign_key="session_table.session_id")

class GetInfoSpeechArray(SQLModel):
    """Информация o речи для отображения на клиенте"""
    speech_id: int = Field(
        title="1",
        description="Идентификатор речи"
    )
    speech_type: SpeechType = Field(
        title="слог",
        description="Биологический тип сигнала"
    )
    is_reference_speech: bool = Field(
        title="true",
        description="Флаг, указывающий на то, является ли речь эталонной"
    )
    real_value: str = Field(
        title="кась",
        description="Реальное значение слога или фразы, которое должно было быть произнесено"
    )

class GetSessionInfo(SQLModel):
    """Информация o сессии"""
    session_score: Optional[float] = Field(
        title="57.5",
        description="Оценка сеанса речевой реабилитации"
    )
    is_reference_session: bool = Field(
        title="true",
        description="Флаг, указывающий на то, является ли сеанс эталонным"
    )
    speech_array: List[GetInfoSpeechArray]

class GetSpeechInfo(SQLModel):
    """Информация o речи"""
    base64_value: str = Field(
        title="UklGRgYvAABXQVZFZm",
        description="Записанный звуковой файл, закодированный в base64"
    )

class GetSessionInfoArray(SQLModel):
    """Информация o сессиях для пациента"""
    session_id: int = Field(
        title="1",
        description="Идентификатор сеанса в базе данных"
    )
    is_reference_session: bool = Field(
        title="true",
        description="Флаг, указывающий на то, является ли сеанс эталонным"
    )
    session_type: SessionType = Field(
        title="фразы",
        description="Тип биологического сигнала, записываемый в рамках одного сеанса"
    )

class GetSessionPatientInfo(SQLModel):
    """Информация o пациенте и его сеансах"""
    get_patient_info: GetPatientInfo
    sessions: List[GetSessionInfoArray]

class GetPhrasesInfo(SQLModel):
    """Информация o фразах и слогах"""
    phrases: List[str]
    syllables: List[str]

class SyllablesPhrasesTable(SQLModel, table=True):
    """Таблица фраз и слогов"""
    __tablename__: str = "syllables_phrases_table"
    syllable_phrase_id: Optional[int] = Field(default=None, primary_key=True)
    syllable_phrase_type: str = Field(
        title="phrase",
        description="Тип (фраза или слог)"
    )
    dict_: str = Field(
        sa_column=Column("dict", String),
        alias='dict',
        title="[к]",
        description="Звук"
    )
    value: str = Field(
        title="День был удивительно хорош",
        description="Значение фразы либо слога"
    )

class SpeechCompareTable(SQLModel, table=True):
    """Таблица сравнения речи"""
    __tablename__: str = "speech_compare_table"
    speech_compare_id: Optional[int] = Field(default=None, primary_key=True)
    speech_id: int = Field(foreign_key="speech_table.speech_id")
    compared_speech_id: int = Field(foreign_key="speech_table.speech_id")
    speech_score: float = Field(
        title="57.5",
        description="Оценка речи"
    )

class SessionCompareTable(SQLModel, table=True):
    """Таблица сравнения сеансов"""
    __tablename__: str = "session_compare_table"
    session_compare_id: Optional[int] = Field(default=None, primary_key=True)
    session_id: int = Field(foreign_key="session_table.session_id")
    compared_session_id: int = Field(foreign_key="session_table.session_id")
    session_score: float = Field(
        title="57.5",
        description="Оценка сеанса"
    )
