import secrets
import string
from pathlib import Path
from transliterate import translit
from audioserver.logic.secactions import hash_gost_3411
from audioserver.logic.audiotools.tools import AudioFile

def generate_password(pass_length: int) -> str:
    """Генерация пароля"""
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for idx in range(pass_length))

    return password

def transliterate_ru_to_en(text: str) -> str:
    """Транслитерация с русского в английский"""

    return translit(text, language_code='ru', reversed=True)

def generate_doctors():
    """Генерация врачей для БД"""

    names = ['Евгений', 'Денис', 'Антон', 'Игорь', 'Юрий', 'Олег', 'Вячеслав',
            'Василий', 'Станислав', 'Вадим',
            'Елена', 'Наталья', 'Ольга', 'Юлия', 'Татьяна', 'Ирина',
            'Светлана', 'Марина', 'Надежда', 'Любовь']

    surnames = ['Иванов', 'Смирнов', 'Кузнецов', 'Попов', 'Васильев', 'Петров',
                'Соколов', 'Михайлов', 'Новиков',
                'Фёдоров', 'Конева', 'Полянская', 'Снегова', 'Карпова', 'Матвеева',
                'Медведева', 'Белая', 'Полякова', 'Фролова', 'Левченко']

    for idx, value in enumerate(names):
        if idx > 10:
            hospital = "Moscow NII_1"
            specialization = "logoped_onkolog"
        else:
            hospital = "Tomsk NII"
            specialization = "logoped"

        print(f"INSERT INTO doctor_table VALUES ('user{idx}', '{specialization}', '{hospital}', '{hash_gost_3411(generate_password(9))}', '{transliterate_ru_to_en(value)} {transliterate_ru_to_en(surnames[idx])}');")

def generate_specialists():
    """Генерация специалистов для БД"""

    for i in range(21, 40):
        print(f"INSERT INTO specialist_table VALUES ('user{i}', '{hash_gost_3411(generate_password(9))}');")

def generate_signal():
    """Генерация звукового сигнала"""

    phrases = ["Белая пелена лежала на полях",
                "В школу приезжали герои фронта",
                "Белый пар расстилается над лужами",
                "Экипаж танка понял задачу",
                "Этот блок работает хорошо",
                "Начинаются степные пожары",
                "Ученики поливают огород",
                "Тяжелый подъем закончился",
                "Тропинка уперлась в глинистый уступ",
                "Солнце поднялось над лесом",
                "В подъезде стояли санитары",
                "Стало известно место встречи",
                "На участке ведется наблюдение",
                "В класс вошел преподаватель",
                "Полено раскололось надвое",
                "Надо зарядить ружье",
                "Телега начала скрипеть",
                "Мать отвела ребенка в сад",
                "Ребята сидели на берегу",
                "В магазине продаются яблоки",
                "Директор сравнил доход с расходом",
                "Высокая рожь колыхалась",
                "Цветы пестрели в долине",
                "Чудный запах леса освежает",
                "День был удивительно хорош"]

    cwd = Path.cwd()
    syllables = cwd / 'slogs'

    for idx, value in enumerate(phrases):
        if idx % 3 != 0:
            is_reference_flag = 1
        else:
            is_reference_flag = 0

        path = syllables / f'{idx+1}.wav'
        audio = AudioFile(path)

        base64 = audio.encode_base64()
        base64_truncated = base64[:150]
        print(f"INSERT INTO signal_table (signal_type, base64_value, is_reference_signal, real_value) VALUES ('фраза', '{base64_truncated}', '{is_reference_flag}', '{value}');")
