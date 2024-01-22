// common routes
export const AUTH = "";
export const DOCTOR = "/doctor/*";
export const PATIENT = "/patient/*";

//routes for doctor

export const DOCTORROOT = "/doctor";

export const PATIENTBASE = "";
export const PATIENTCHANGEPASS = "change/";
export const PATIENTCARD = "/card/:patientID";
export const PATIENTSPEECHLIST = "/card/:patientID/:type/:flag/:session";

//routes for patient

export const PATIENTROOT = "/patient";
export const DOCTORCARDFORPATIENT = "/card";
export const PATIENTSPEECHLISTP = "/card/:patientID/:type/:flag/:session";
export const DOCTORBASE = "";
