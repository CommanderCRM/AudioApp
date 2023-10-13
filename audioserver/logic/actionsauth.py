import uuid
import datetime
import base64
import hmac
import hashlib
import json
from pygost.gost34112012 import GOST34112012

JWT_KEY = "8694c19e-17d7-4479-88eb-402c07fea387"

def validate_pass(password):
    """Валидация пароля"""
    special_chars=r"!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    numbers="01234567890"

    if (any(c in special_chars for c in password)
        and any(c in numbers for c in password)):
        return True

    return False

def hash_gost_3411(password):
    """Хэширование пароля по ГОСТ 34.11-2018 (256 бит)"""
    m = GOST34112012(digest_size=256)
    pass_bytes = str.encode(password)
    m.update(pass_bytes)

    return m.hexdigest()

def generate_exp_date(exp_type):
    """Расчет даты от текущего момента (короткий, длинный периоды)"""
    current_datetime = datetime.datetime.now()

    if exp_type == 'short':
        datetime_in_30_min = current_datetime + datetime.timedelta(minutes=30)
        formatted_datetime_in_30_min = datetime_in_30_min.strftime('%Y%m%d%H%M')
        return formatted_datetime_in_30_min

    if exp_type == 'long':
        datetime_in_30_days = current_datetime + datetime.timedelta(days=30)
        formatted_datetime_in_30_days = datetime_in_30_days.strftime('%Y%m%d%H%M')
        return formatted_datetime_in_30_days

    return False

def encode_and_sign_jwt(header, payload, secret):
    """Кодирование тела JWT и его подпись"""
    byte_header = json.dumps(header).encode()
    byte_payload = json.dumps(payload).encode()

    encoded_header = base64.urlsafe_b64encode(byte_header).rstrip(b'=').decode()
    encoded_payload = base64.urlsafe_b64encode(byte_payload).rstrip(b'=').decode()

    message = f'{encoded_header}.{encoded_payload}'.encode()
    signature = hmac.new(secret, message, hashlib.sha256).digest()
    encoded_signature = base64.urlsafe_b64encode(signature).rstrip(b'=').decode()

    return encoded_header, encoded_payload, encoded_signature

def generate_jwt(user, role, exp_type):
    """Генерация JWT токена"""

    # Заголовок
    alg = 'HS256'
    typ = 'JWT'
    header = {"alg": alg, "typ": typ}

    # Полезные данные
    jwt_uuid = str(uuid.uuid4())
    jwt_user = user
    jwt_role = role
    if exp_type == 'short':
        jwt_exp = generate_exp_date('short')
    elif exp_type == 'long':
        jwt_exp = generate_exp_date('long')
    payload = {"uuid": jwt_uuid, "user": jwt_user, "role": jwt_role, "exp": jwt_exp}

    # Секрет
    secret = bytes(JWT_KEY, encoding='UTF-8')

    # base64 заголовок, тело + подпись
    encoded_header, encoded_payload, encoded_signature = encode_and_sign_jwt(header, payload, secret)

    jwt = f"{encoded_header}.{encoded_payload}.{encoded_signature}"
    return jwt
