CREATE TABLE PatientTable (
  MedicalCardNumber INT PRIMARY KEY,
  FullName VARCHAR(255),
  Gender CHAR(1),
  ConstantPassword VARCHAR(128),
  TemporaryPassword VARCHAR(128),
  IsPasswordChanged BOOL
);

CREATE TABLE ReferenceTable (
  ReferenceId serial PRIMARY KEY,
  ReferenceName VARCHAR(50),
  Type VARCHAR(50),
  MedicalCardNumber int REFERENCES PatientTable(MedicalCardNumber),
  Base64Audio VARCHAR
);

CREATE TABLE DistoredSpeechTable (
  DistoredSpeechId serial PRIMARY KEY,
  Type VARCHAR(50),
  MedicalCardNumber int REFERENCES PatientTable(MedicalCardNumber),
  Base64Audio VARCHAR
);

CREATE TABLE SpeechQualityTable (
  SpeechQualityId serial PRIMARY KEY,
  Score int,
  ReferenceId int REFERENCES ReferenceTable(ReferenceId),
  DistoredSpeechId int REFERENCES DistoredSpeechTable(DistoredSpeechId)
);

CREATE TABLE SessionTable (
  SessionId serial PRIMARY KEY,
  MedicalCardNumber int REFERENCES PatientTable(MedicalCardNumber)
);

CREATE TABLE SpeechQualitySessionTable (
  SpeechQualitySessionId serial PRIMARY KEY,
  SpeechQualityId int REFERENCES SpeechQualityTable(SpeechQualityId),
  SessionId int REFERENCES SessionTable(SessionId)
);
