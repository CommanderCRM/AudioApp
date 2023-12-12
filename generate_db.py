import secrets
import string
from transliterate import translit
from audioserver.logic.secactions import hash_gost_3411

def generate_doctors():
    """Генерация врачей для БД"""
    alphabet = string.ascii_letters + string.digits

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
            print(f"INSERT INTO doctor_table VALUES ('user{idx}', 'logoped', 'Moscow NII_1', '{hash_gost_3411(''.join(secrets.choice(alphabet) for i in range(9)))}', '{translit(value, language_code='ru', reversed=True)} {translit(surnames[idx], language_code='ru', reversed=True)}');")
        else:
            print(f"INSERT INTO doctor_table VALUES ('user{idx}', 'logoped onkolog', 'Tomsk NII', '{hash_gost_3411(''.join(secrets.choice(alphabet) for i in range(9)))}', '{translit(value, language_code='ru', reversed=True)} {translit(surnames[idx], language_code='ru', reversed=True)}');")

generate_doctors()