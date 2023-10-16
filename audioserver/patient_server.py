from enum import Enum
from fastapi import FastAPI, status, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from logic.tables import PostSpeechInfo, TemporaryPasswordChangePatientInfo
from logic.actions import (insert_speech, select_phrases_and_syllables,
                           select_password_status, get_doctors_list)
from logic.actionspatientauth import (change_temporary_password, check_access_token,
                                      get_username_from_token)

app = FastAPI()

class ErrorCode(Enum):
    """Типы ошибок"""
    CARD_EXISTS = 1
    CONST_PASS_WITH_UNCHANGED_FLAG = 3
    TEMP_PASS_WITH_CHANGED_FLAG = 4
    INTERNAL_SERVER_ERROR = 5
    API_VALIDATION_ERROR = 6

@app.exception_handler(HTTPException)
async def internal_server_error_handler(_, exception: HTTPException):
    """Обработка внутренней ошибки сервера 500"""
    if exception.status_code == 500:
        return JSONResponse(content={"result_code": ErrorCode.INTERNAL_SERVER_ERROR.value},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # Все остальное уходит в обычную обработку ошибок
    return await app.exception_handler(exception)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, __):
    """Обработка ошибки валидации данных"""
    return JSONResponse(content={"result_code": ErrorCode.API_VALIDATION_ERROR.value},
                            status_code=status.HTTP_400_BAD_REQUEST)

async def get_token_from_header(request: Request):
    """Получение токена доступа из заголовка"""
    auth_header = request.headers.get('Authorization')

    if auth_header:
        access_token = auth_header.replace("Bearer ", "")

    return access_token

async def send_token_for_check(request: Request):
    """Отправка токена доступа на проверку"""
    access_token = await get_token_from_header(request)

    return check_access_token(access_token)

@app.post("/session/{session_id}")
async def upload_record_speech(session_id: int, speech_info: PostSpeechInfo):
    """Загрузить/записать речь в сеанс"""

    return insert_speech(None, session_id, speech_info)

@app.get("/session/{session_id}")
async def get_phrases_and_syllables_info():
    """Получить информацию o фразах и слогах"""

    return select_phrases_and_syllables()

@app.get("/login")
async def get_password_status(card_number: str):
    """Получить информацию о статусе пароля"""

    return select_password_status(card_number)

@app.patch("/login")
async def temporary_password_change(request: Request):
    """Изменить временный пароль на постоянный"""
    data = await request.json()
    login_info = TemporaryPasswordChangePatientInfo(**data)

    return change_temporary_password(login_info.card_number, login_info.constant_password,
                                      login_info.temporary_password)

@app.get("/info")
async def get_doctors_info(request: Request):
    """Получение информации о лечащих врачах"""
    if await send_token_for_check(request):
        access_token = await get_token_from_header(request)
        username = get_username_from_token(access_token)
        return get_doctors_list(username)
