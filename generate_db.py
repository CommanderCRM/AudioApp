import random
from transliterate import translit, get_available_language_codes
from audioserver.logic.secactions import hash_gost_3411
import secrets
import string
alphabet = string.ascii_letters + string.digits

names = ['Евгений', 'Денис', 'Антон', 'Игорь', 'Юрий', 'Олег', 'Вячеслав', 'Василий', 'Станислав', 'Вадим', 'Елена', 'Наталья', 'Ольга', 'Юлия', 'Татьяна', 'Ирина', 'Светлана', 'Марина', 'Надежда', 'Любовь']
surnames = ['Иванов', 'Смирнов', 'Кузнецов', 'Попов', 'Васильев', 'Петров', 'Соколов', 'Михайлов', 'Новиков', 'Фёдоров', 'Конева', 'Полянская', 'Снегова', 'Карпова', 'Матвеева', 'Медведева', 'Белая', 'Полякова', 'Фролова', 'Левченко']

for i in range(len(names)):
    if i > 10:
        print(f"INSERT INTO doctor_table VALUES ('user{i}', 'logoped', 'Moscow NII_1', '{hash_gost_3411(''.join(secrets.choice(alphabet) for i in range(9)))}', '{translit(names[i], language_code='ru', reversed=True)} {translit(surnames[i], language_code='ru', reversed=True)}');")
    else:
        print(f"INSERT INTO doctor_table VALUES ('user{i}', 'logoped onkolog', 'Tomsk NII', '{hash_gost_3411(''.join(secrets.choice(alphabet) for i in range(9)))}', '{translit(names[i], language_code='ru', reversed=True)} {translit(surnames[i], language_code='ru', reversed=True)}');")