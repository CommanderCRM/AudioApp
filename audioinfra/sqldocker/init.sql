CREATE TABLE patientTable (
  medicalCardNumber VARCHAR(12) PRIMARY KEY,
  fullName VARCHAR(255),
  gender CHAR(1),
  constantPassword VARCHAR(128),
  temporaryPassword VARCHAR(128),
  isPasswordChanged BOOL,
  dateOfBirth DATE
);

CREATE TABLE referenceTable (
  referenceId serial PRIMARY KEY,
  referenceName VARCHAR(50),
  type VARCHAR(50),
  medicalCardNumber VARCHAR(12) REFERENCES patientTable(medicalCardNumber),
  base64Value VARCHAR
);

CREATE TABLE distoredSpeechTable (
  distoredSpeechId serial PRIMARY KEY,
  type VARCHAR(50),
  medicalCardNumber VARCHAR(12) REFERENCES patientTable(medicalCardNumber),
  base64Value VARCHAR
);

CREATE TABLE speechQualityTable (
  speechQualityId serial PRIMARY KEY,
  score int,
  referenceId int REFERENCES referenceTable(referenceId),
  distoredSpeechId int REFERENCES distoredSpeechTable(distoredSpeechId)
);

CREATE TABLE sessionTable (
  sessionId serial PRIMARY KEY,
  medicalCardNumber VARCHAR(12) REFERENCES patientTable(medicalCardNumber)
);

CREATE TABLE speechQualitySessionTable (
  speechQualitySessionId serial PRIMARY KEY,
  speechQualityId int REFERENCES speechQualityTable(speechQualityId),
  sessionId int REFERENCES sessionTable(sessionId)
);
