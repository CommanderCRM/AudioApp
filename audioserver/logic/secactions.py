import datetime
import jwt
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
    """Хэширование пароля по ГОСТ 34.11-2018 (512 бит / 64 байта)"""
    m = GOST34112012(digest_size=64)
    pass_bytes = str.encode(password)
    m.update(pass_bytes)

    return m.hexdigest()

def generate_exp_date(exp_type):
    """Расчет даты от текущего момента (короткий, длинный периоды)"""
    current_datetime = datetime.datetime.now()

    if exp_type == 'short':
        datetime_in_30_min = current_datetime + datetime.timedelta(minutes=30)
        return datetime_in_30_min

    if exp_type == 'long':
        datetime_in_30_days = current_datetime + datetime.timedelta(days=30)
        return datetime_in_30_days

    return False

def generate_jwt(generated_uuid, user, role, exp_type):
    """Генерация JWT токена"""

    # Полезные данные
    jwt_uuid = generated_uuid
    jwt_user = user
    jwt_role = role

    if exp_type == 'short':
        jwt_exp = generate_exp_date('short')
    elif exp_type == 'long':
        jwt_exp = generate_exp_date('long')

    payload = {"uuid": jwt_uuid, "user": jwt_user, "role": jwt_role, "exp": jwt_exp}

    token = jwt.encode(payload, JWT_KEY, algorithm='HS256')

    return token
