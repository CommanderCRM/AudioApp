CREATE TABLE patient_table (
  card_number TEXT PRIMARY KEY,
  full_name TEXT,
  gender TEXT,
  constant_password TEXT,
  hospital TEXT,
  temporary_password TEXT,
  is_password_changed INTEGER,
  date_of_birth TEXT,
  patient_info TEXT
);

CREATE TABLE speech_table (
  speech_id INTEGER PRIMARY KEY AUTOINCREMENT,
  speech_type TEXT,
  base64_value TEXT,
  base64_segment_value TEXT,
  is_reference_speech INTEGER,
  real_value TEXT
);

CREATE TABLE speech_compare_table (
  speech_compare_id INTEGER PRIMARY KEY AUTOINCREMENT,
  speech_id INTEGER,
  compared_speech_id INTEGER,
  speech_score REAL,
  FOREIGN KEY(speech_id) REFERENCES speech_table(speech_id),
  FOREIGN KEY(compared_speech_id) REFERENCES speech_table(speech_id)
);

CREATE TABLE session_table (
  session_id INTEGER PRIMARY KEY AUTOINCREMENT,
  is_reference_session INTEGER,
  session_type TEXT,
  card_number TEXT,
  FOREIGN KEY(card_number) REFERENCES patient_table(card_number)
);

CREATE TABLE session_compare_table (
  session_compare_id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id INTEGER,
  compared_session_id INTEGER,
  session_score REAL,
  FOREIGN KEY(session_id) REFERENCES session_table(session_id),
  FOREIGN KEY(compared_session_id) REFERENCES session_table(session_id)
);

CREATE TABLE speech_session_table (
  speech_session_id INTEGER PRIMARY KEY AUTOINCREMENT,
  speech_id INTEGER,
  session_id INTEGER,
  FOREIGN KEY(speech_id) REFERENCES speech_table(speech_id),
  FOREIGN KEY(session_id) REFERENCES session_table(session_id)
);

CREATE TABLE doctor_table (
  username TEXT PRIMARY KEY,
  specialization TEXT,
  hospital TEXT,
  password TEXT,
  full_name TEXT
);

CREATE TABLE specialist_table (
  username TEXT PRIMARY KEY,
  password TEXT
);

CREATE TABLE doctor_patient_table (
  doctor_patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
  doctor_username TEXT,
  patient_card_number TEXT,
  FOREIGN KEY(doctor_username) REFERENCES doctor_table(username),
  FOREIGN KEY(patient_card_number) REFERENCES patient_table(card_number)
);

CREATE TABLE syllables_phrases_table (
  syllable_phrase_id INTEGER PRIMARY KEY AUTOINCREMENT,
  syllable_phrase_type TEXT,
  dict TEXT,
  value TEXT
);

INSERT INTO doctor_table VALUES ('user1', 'logoped', 'Tomsk NII', 'ba12f65801cc7cec593c311bd1bb4d9a72fcc84059e36e0c642', 'Ilia Krivosh');
INSERT INTO doctor_table VALUES ('user2', 'logoped onkolog', 'Tomsk NII', 'ba12f65801cc7cec593c311bd1bb4d9a72fcc6', 'Ilia Bebrov');

INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','Белая пелена лежала на полях');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','В школу приезжали герои	фронта');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','Белый пар расстилается над лужами');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','Экипаж танка понял задачу');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','Этот блок работает хорошо');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','Начинаются степные пожары');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','Ученики поливают огород');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','Тяжелый подъем закончился');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','Тропинка уперлась в глинистый уступ');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','Солнце поднялось над лесом');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','В подъезде стояли санитары');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','Стало известно место встречи');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','На участке ведется наблюдение');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','В класс вошел преподаватель');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','Полено раскололось надвое');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','Надо зарядить ружье');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','Телега начала скрипеть');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','Мать отвела ребенка в сад');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','Ребята сидели на берегу');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','В магазине продаются яблоки');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','Директор сравнил доход с расходом');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','Высокая рожь колыхалась');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','Цветы пестрели в долине');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','Чудный запах леса освежает');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','День был удивительно хорош');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('syllable','[к]','кась');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('syllable','[к`]','кясь');

SELECT * FROM doctor_table;
SELECT * FROM syllables_phrases_table;
