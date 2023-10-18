-- DDL Generated from https:/databasediagram.com

CREATE TABLE patient_table (
  card_number VARCHAR(12) PRIMARY KEY,
  full_name VARCHAR(255),
  gender CHAR(1),
  constant_password VARCHAR(128),
  hospital VARCHAR(64),
  temporary_password VARCHAR(128),
  is_password_changed BOOL,
  date_of_birth DATE
);

CREATE TABLE speech_table (
  speech_id SERIAL PRIMARY KEY,
  speech_type VARCHAR(50),
  base64_value VARCHAR,
  base64_segment_value VARCHAR,
  is_reference_speech BOOL,
  real_value VARCHAR(50)
);

CREATE TABLE speech_compare_table (
  speech_compare_id SERIAL PRIMARY KEY,
  compared_speech_id_1 INT REFERENCES speech_table(speech_id),
  compared_speech_id_2 INT REFERENCES speech_table(speech_id),
  compared_speech_id_3 INT REFERENCES speech_table(speech_id),
  speech_score REAL
);

CREATE TABLE session_table (
  session_id SERIAL PRIMARY KEY,
  is_reference_session BOOL,
  session_type VARCHAR(50),
  card_number VARCHAR(12) REFERENCES patient_table(card_number)
);

CREATE TABLE session_compare_table (
  session_compare_id SERIAL PRIMARY KEY,
  compared_session_id_1 INT REFERENCES session_table(session_id),
  compared_session_id_2 INT REFERENCES session_table(session_id),
  compared_session_id_3 INT REFERENCES session_table(session_id),
  session_score REAL
);

CREATE TABLE speech_session_table (
  speech_session_id SERIAL PRIMARY KEY,
  speech_id int REFERENCES speech_table(speech_id),
  session_id int REFERENCES session_table(session_id)
);

CREATE TABLE doctor_table (
  username VARCHAR(255) PRIMARY KEY,
  specialization VARCHAR(255),
  hospital VARCHAR(64),
  password VARCHAR(128),
  full_name VARCHAR(255)
);

CREATE TABLE specialist_table (
  username VARCHAR(255) PRIMARY KEY,
  password VARCHAR(128)
);

CREATE TABLE doctor_patient_table (
  doctor_patient_id SERIAL PRIMARY KEY,
  doctor_username VARCHAR(255) REFERENCES doctor_table(username),
  patient_card_number VARCHAR(12) REFERENCES patient_table(card_number)
);

CREATE TABLE syllables_phrases_table (
  syllable_phrase_id SERIAL PRIMARY KEY,
  syllable_phrase_type VARCHAR(10),
  dict VARCHAR(10),
  value VARCHAR(50)
);

CREATE TABLE refresh_token_table (
  refresh_token_id SERIAL PRIMARY KEY,
  token UUID,
  username VARCHAR(255),
  exp INT,
  role VARCHAR(20)
);

INSERT INTO doctor_table VALUES ('user1', 'logoped', 'Tomsk NII', 'f42d8ccc9d8a783bd8d5cf417afa8953dbc92c338c7ea92ae88785fe50271714', 'Ilia Krivosh');
INSERT INTO doctor_table VALUES ('user2', 'logoped onkolog', 'Tomsk NII', '31f2fd3efdf395d9d2d958367b74ace5b8539b31c45e8b1b39a622a07d5b8097', 'Ilia Bebrov');
INSERT INTO specialist_table VALUES ('user3', '75b9eb6eb3b5f5ddeb3176ecd1de99b12821a838144374cce0537f03c0500e52');

INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','Белая пелена лежала на полях');
INSERT INTO syllables_phrases_table (syllable_phrase_type, dict, value) VALUES ('phrase','phrases','В школу приезжали герои фронта');
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
