from enum import Enum
from fastapi import FastAPI, status, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from logic.tables import (PostSpeechInfo, TemporaryPasswordChangePatientInfo, TokenObject,
                          PasswordPatientInfo, PostSessionInfoPatient, PostSessionInfo,
                          PasswordChangePatientInfo)
from logic.actions import (insert_speech, select_phrases_and_syllables,
                           select_password_status, get_doctors_list, insert_session_info)
from logic.actionspatientauth import (change_temporary_password, check_token,
                                      get_username_from_token, create_two_tokens,
                                      delete_refresh_token, get_uuid_from_token,
                                      check_patient_and_login, change_const_patient_password)

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

async def get_token_from_cookie(request: Request):
    """Получение токена обновления из cookie"""
    refresh_token = request.cookies.get('refresh_token')

    return refresh_token

async def send_access_token_for_check(request: Request):
    """Отправка токена доступа на проверку"""
    access_token = await get_token_from_header(request)

    return check_token(access_token)

async def send_refresh_token_for_check(request: Request):
    """Отправка токена обновления на проверку"""
    refresh_token = await get_token_from_cookie(request)

    return check_token(refresh_token)

@app.post("/session")
async def create_speech_session(request: Request):
    """Создание сеанса записи речи"""
    if await send_access_token_for_check(request):
        data = await request.json()
        session_info_patient = PostSessionInfoPatient(**data)
        session_type = session_info_patient.session_type

        access_token = await get_token_from_header(request)
        username = get_username_from_token(access_token)

        session_info = PostSessionInfo(is_reference_session=False, session_type=session_type)

        return insert_session_info(username, session_info)

@app.post("/session/{session_id}")
async def upload_record_speech(request: Request, session_id: int, speech_info: PostSpeechInfo):
    """Загрузить/записать речь в сеанс"""
    if await send_access_token_for_check(request):
        return insert_speech(None, session_id, speech_info)

@app.get("/session/{session_id}")
async def get_phrases_and_syllables_info(request: Request):
    """Получить информацию o фразах и слогах"""
    if await send_access_token_for_check(request):
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
    if await send_access_token_for_check(request):
        access_token = await get_token_from_header(request)
        username = get_username_from_token(access_token)

        return get_doctors_list(username)

@app.post("/update_tokens")
async def update_tokens(request: Request):
    """Обновление пары токенов"""
    if await send_refresh_token_for_check(request):
        refresh_token = await get_token_from_cookie(request)
        username = get_username_from_token(refresh_token)
        token_uuid = get_uuid_from_token(refresh_token)

        delete_refresh_token(token_uuid)

        short_jwt, long_jwt = create_two_tokens(username)

        return TokenObject(access_token=short_jwt, refresh_token=long_jwt)

@app.post("/login")
async def login_patient(request: Request):
    """Вход пациента в систему"""
    data = await request.json()
    login_info = PasswordPatientInfo(**data)

    return check_patient_and_login(login_info.card_number, login_info.constant_password)

@app.patch("/settings")
async def change_patient_password(request: Request):
    """Смена постоянного пароля пациента на другой постоянный"""
    if await send_access_token_for_check(request):
        data = await request.json()
        change_info = PasswordChangePatientInfo(**data)

        return change_const_patient_password(change_info.card_number,
                                             change_info.old_password, change_info.new_password)

@app.get("/logout")
async def logout_patient(request: Request):
    """Выход пациента из системы"""
    if await send_refresh_token_for_check(request):
        refresh_token = await get_token_from_cookie(request)
        token_uuid = get_uuid_from_token(refresh_token)

        delete_refresh_token(token_uuid)
