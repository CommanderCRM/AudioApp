import secrets
import string
from transliterate import translit
from audioserver.logic.secactions import hash_gost_3411

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
        else:
            hospital = "Tomsk NII"

        print(f"INSERT INTO doctor_table VALUES ('user{idx}', 'logoped', '{hospital}', '{hash_gost_3411(generate_password(9))}', '{transliterate_ru_to_en(value)} {transliterate_ru_to_en(surnames[idx])}');")

def generate_specialists():
    """Генерация специалистов для БД"""
    return

generate_doctors()
