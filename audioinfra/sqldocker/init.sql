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

INSERT INTO doctor_table VALUES ('user1', 'logoped', 'Tomsk NII', 'e2fb95ed6eab55bec760d47cae055a38b7753459e4151dd546c01e0f1af7fafe84c61f4051e783091517c0054c7655fdada36cd631c38971e3f46797e81890ce', 'Ilia Krivosh');
INSERT INTO doctor_table VALUES ('user2', 'logoped onkolog', 'Tomsk NII', 'd55efc9dd983fcb3911dff5ea08776cdab9cf6275b8bcc04ab4297d7b93f862808a9843daa377a3de7a404c15042c416f847a0889fc5af4362e5d4a2826a9f0e', 'Ilia Bebrov');
INSERT INTO specialist_table VALUES ('user3', '696560849678c23b9c51b4c0f95cec5a3f5d85d75fc4f93151fe897bf252a0fd6807699a6720dd3ee094414f7d5d6f5cbd73ce338491e6780e798d925f34f09f');

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
