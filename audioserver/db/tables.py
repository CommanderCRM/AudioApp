from typing import Optional
from sqlmodel import Field, SQLModel

class PatientTable(SQLModel, table=True):
    '''Таблица пациента'''
    medicalcardnumber: int = Field(default=None, primary_key=True)
    fullname: str
    gender: str
    constantpassword: Optional[str] = None
    temporarypassword: Optional[str] = None
    ispasswordchanged: bool
