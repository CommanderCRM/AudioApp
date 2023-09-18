CREATE TABLE patient_table (
  medical_card_number VARCHAR(12) PRIMARY KEY,
  full_name VARCHAR(255),
  gender CHAR(1),
  constant_password VARCHAR(128),
  temporary_password VARCHAR(128),
  is_password_changed BOOL,
  date_of_birth DATE,
  town VARCHAR(64)
);

CREATE TABLE reference_table (
  reference_id serial PRIMARY KEY,
  reference_name VARCHAR(50),
  referenct_type VARCHAR(50),
  medical_card_number VARCHAR(12) REFERENCES patient_table(medical_card_number),
  base64_value VARCHAR
);

CREATE TABLE speech_table (
  speech_id serial PRIMARY KEY,
  speech_type VARCHAR(50),
  medical_card_number VARCHAR(12) REFERENCES patient_table(medical_card_number),
  base64_value VARCHAR
);

CREATE TABLE speech_quality_table (
  speech_quality_id serial PRIMARY KEY,
  score int,
  reference_id int REFERENCES reference_table(reference_id),
  speech_id int REFERENCES speech_table(speech_id)
);

CREATE TABLE session_table (
  session_id serial PRIMARY KEY,
  medical_card_number VARCHAR(12) REFERENCES patient_table(medical_card_number)
);

CREATE TABLE speech_quality_session_table (
  speech_quality_session_id serial PRIMARY KEY,
  speech_quality_id int REFERENCES speech_quality_table(speech_quality_id),
  session_id int REFERENCES session_table(session_id)
);

CREATE TABLE doctor_table (
  username VARCHAR(255) PRIMARY KEY,
  specialization VARCHAR(255),
  town VARCHAR(64),
  password VARCHAR(128),
  full_name VARCHAR(255)
);

CREATE TABLE specialist_table (
  username VARCHAR(255) PRIMARY KEY,
  password VARCHAR(128)
);
