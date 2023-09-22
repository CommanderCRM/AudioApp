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
  speech_id serial PRIMARY KEY,
  speech_type VARCHAR(50),
  base64_value VARCHAR,
  base64_segmet_value VARCHAR,
  speech_score REAL,
  is_reference_speech BOOL
);

CREATE TABLE session_table (
  session_id serial PRIMARY KEY,
  is_reference_session BOOL,
  session_score REAL,
  card_number VARCHAR(12) REFERENCES patient_table(card_number)
);

CREATE TABLE speech_session_table (
  speech_session_id serial PRIMARY KEY,
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
  doctor_patient_id serial PRIMARY KEY,
  doctor_username VARCHAR(255) REFERENCES doctor_table(username),
  patient_card_number VARCHAR(12) REFERENCES patient_table(card_number)
);

CREATE TABLE syllables_phrases_table (
  syllable_phrase_id serial PRIMARY KEY,
  type VARCHAR(10),
  dict VARCHAR(10),
  value VARCHAR(50),
  start_position int,
  end_position int
);
