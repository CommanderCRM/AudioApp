from enum import Enum
from fastapi import FastAPI, status, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from logic.tables import (PostPatientInfo, PostSessionInfo, PostSpeechInfo,
                          CompareSessionsIDs, TokenObject, PasswordChangeInfo, LoginInfo)
from logic.actions import (insert_patient, select_all_patients, select_patient_by_key,
                        convert_full_model_to_table, insert_session_info, insert_speech,
                        select_session_info, select_speech_info, select_session_by_key,
                        select_patient_and_sessions, select_phrases_and_syllables,
                        compare_two_sessions, compare_phrases_real)
from logic.actionsauth import (check_token, get_username_from_token, get_uuid_from_token,
                               check_data_and_login, change_const_password, delete_refresh_token,
                               create_two_tokens, get_role_from_token)

app = FastAPI()

# Перенаправляем весь трафик на HTTPS
app.add_middleware(HTTPSRedirectMiddleware)

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

@app.post("/patients")
async def create_patient(patient: PostPatientInfo, request: Request):
    """Создание пациента по запросу POST"""
    if await send_access_token_for_check(request):
        access_token = await get_token_from_header(request)
        role = get_role_from_token(access_token)

        if role == 'doctor':
            patient_table, doctor_patient_list = convert_full_model_to_table(patient)

            if select_patient_by_key(patient_table.card_number):
                return JSONResponse(content={"result_code": ErrorCode.CARD_EXISTS.value},
                                    status_code=status.HTTP_400_BAD_REQUEST)

            if not patient_table.is_password_changed and patient_table.constant_password:
                return JSONResponse(content={"result_code": ErrorCode.CONST_PASS_WITH_UNCHANGED_FLAG.value},
                                    status_code=status.HTTP_400_BAD_REQUEST)

            if patient_table.is_password_changed and patient_table.temporary_password:
                return JSONResponse(content={"result_code": ErrorCode.TEMP_PASS_WITH_CHANGED_FLAG.value},
                                    status_code=status.HTTP_400_BAD_REQUEST)

            return insert_patient(patient_table, doctor_patient_list)

@app.get("/patients")
async def get_patients(limit: int, request: Request):
    """Получение пациентов по запросу GET"""
    if await send_access_token_for_check(request):
        access_token = await get_token_from_header(request)
        role = get_role_from_token(access_token)

        if role in {'doctor', 'specialist'}:
            return select_all_patients(limit)

@app.post("/patients/{card_number}")
async def post_session_info(card_number: str, session_info: PostSessionInfo, request: Request):
    """Добавить информацию o сеансе"""
    if await send_access_token_for_check(request):
        access_token = await get_token_from_header(request)
        role = get_role_from_token(access_token)

        if role in {'doctor', 'specialist'}:
            if not select_patient_by_key(card_number):
                raise HTTPException(status_code=404)

            return insert_session_info(card_number, session_info)

@app.post("/patients/{card_number}/speech/{session_id}")
async def upload_record_speech(card_number: str, session_id: int, speech_info: PostSpeechInfo, request: Request):
    """Загрузить/записать речь в сеанс"""
    if await send_access_token_for_check(request):
        access_token = await get_token_from_header(request)
        role = get_role_from_token(access_token)

        if role in {'doctor', 'specialist'}:
            if not select_patient_by_key(card_number):
                raise HTTPException(status_code=404)

            return insert_speech(card_number, session_id, speech_info)

@app.get("/patients/{card_number}/session/{session_id}")
async def get_session_info(card_number: str, session_id: int, request: Request):
    """Получить информацию o сессии"""
    if await send_access_token_for_check(request):
        access_token = await get_token_from_header(request)
        role = get_role_from_token(access_token)

        if role in {'doctor', 'specialist'}:
            return select_session_info(card_number, session_id)

@app.get("/patients/{card_number}/session/{session_id}/speech/{speech_id}")
async def get_speech_info(card_number: str, session_id: int, speech_id: int, request: Request):
    """Получить информацию o речи"""
    if await send_access_token_for_check(request):
        access_token = await get_token_from_header(request)
        role = get_role_from_token(access_token)

        if role in {'doctor', 'specialist'}:
            if not select_patient_by_key(card_number) or not select_session_by_key(session_id):
                raise HTTPException(status_code=404)

            return select_speech_info(card_number, session_id, speech_id)

@app.get("/patients/{card_number}")
async def get_patient_and_sessions(card_number: str, request: Request):
    """Получить информацию o пациенте и ero сеансах"""
    if await send_access_token_for_check(request):
        access_token = await get_token_from_header(request)
        role = get_role_from_token(access_token)

        if role in {'doctor', 'specialist'}:
            return select_patient_and_sessions(card_number)

@app.get("/patients/{card_number}/session/{session_id}/speech")
async def get_phrases_and_syllables_info(request: Request):
    """Получить информацию o фразах и слогах"""
    if await send_access_token_for_check(request):
        access_token = await get_token_from_header(request)
        role = get_role_from_token(access_token)

        if role in {'doctor', 'specialist'}:
            return select_phrases_and_syllables()

@app.patch("/patients/{card_number}/session")
async def compare_sessions(card_number: int, request: Request):
    """Сравнение сеансов (аудиофайлы)"""
    if await send_access_token_for_check(request):
        access_token = await get_token_from_header(request)
        role = get_role_from_token(access_token)

        if role in {'doctor', 'specialist'}:
            data = await request.json()
            session_ids = CompareSessionsIDs(**data)

            session_1_id = session_ids.sessions_id[0]
            session_2_id = session_ids.sessions_id[1]

            if not select_session_by_key(session_1_id) or not select_session_by_key(session_2_id):
                raise HTTPException(status_code=404)

            return compare_two_sessions(card_number, session_1_id, session_2_id)

@app.patch("/patients/{card_number}/session/{session_id}")
async def compare_phrases_with_real(card_number: int, session_id: int, request: Request):
    """Сравнение фраз с реальными значениями"""
    if await send_access_token_for_check(request):
        access_token = await get_token_from_header(request)
        role = get_role_from_token(access_token)

        if role in {'doctor', 'specialist'}:
            return compare_phrases_real(card_number, session_id)

@app.post("/update_tokens")
async def update_tokens(request: Request):
    """Обновление пары токенов"""
    if await send_refresh_token_for_check(request):
        refresh_token = await get_token_from_cookie(request)
        username = get_username_from_token(refresh_token)
        token_uuid = get_uuid_from_token(refresh_token)
        role = get_role_from_token(refresh_token)

        if role in {'doctor', 'specialist'}:
            delete_refresh_token(token_uuid)

            short_jwt, long_jwt = create_two_tokens(username, role)

            return TokenObject(access_token=short_jwt, refresh_token=long_jwt)

@app.post("/login")
async def login(request: Request):
    """Вход врача/специалиста в систему"""
    data = await request.json()
    login_info = LoginInfo(**data)

    return check_data_and_login(login_info.username, login_info.password)

@app.patch("/settings")
async def change_const_doct_spec_password(request: Request):
    """Смена постоянного пароля врача/специалиста на другой постоянный"""
    if await send_access_token_for_check(request):
        access_token = await get_token_from_header(request)
        role = get_role_from_token(access_token)

        if role in {'doctor', 'specialist'}:
            data = await request.json()
            change_info = PasswordChangeInfo(**data)

            return change_const_password(change_info.username,
                                                change_info.old_password, change_info.new_password,
                                                role)

@app.get("/logout")
async def logout(request: Request):
    """Выход врача/специалиста из системы"""
    if await send_refresh_token_for_check(request):
        refresh_token = await get_token_from_cookie(request)

        role = get_role_from_token(refresh_token)
        token_uuid = get_uuid_from_token(refresh_token)

        if role in {'doctor', 'specialist'}:
            delete_refresh_token(token_uuid)
