import { AuthPage } from "../pages/auth";
import { DoctorRoot } from "../pages/doctor";
import { DoctorMainPage } from "../pages/doctor/views/doctorMain";
import { PatientCardPage } from "../pages/doctor/views/patientCard";
import { ClientMain } from "../pages/client/views/clientMain";
import { DoctorCardPage } from "../pages/client/views/doctorCard";
import { ChangePassPage } from "../pages/client/views/changePass";
import {
  AUTH,
  DOCTOR,
  DOCTORBASE,
  PATIENT,
  PATIENTBASE,
  PATIENTCARD,
  PATIENTCHANGEPASS,
  PATIENTSPEECHLIST,
  PATIENTSPEECHLISTP,
} from "./const";

import { PatientRoot } from "../pages/client";
import { SessionCard } from "../pages/doctor/views/sessionCard";
import { SessionCardP } from "../pages/client/views/sessionCardClient";

//common paths & components
export const MainURL = [
  {
    Component: AuthPage,
    path: AUTH,
  },
  {
    Component: DoctorRoot,
    path: DOCTOR,
  },
  {
    Component: PatientRoot,
    path: PATIENT,
  },
];

//doctor's paths & components
export const DoctorURL = [
  {
    Component: DoctorMainPage,
    path: DOCTORBASE,
  },
  {
    Component: PatientCardPage,
    path: PATIENTCARD,
  },

  {
    Component: SessionCard,
    path: PATIENTSPEECHLIST,
  },
];

//patient's paths & components
export const PatientURL = [
  {
    Component: ClientMain,
    path: PATIENTBASE,
  },
  {
    Component: DoctorCardPage,
    path: PATIENTCARD,
  },
  {
    Component: ChangePassPage,
    path: PATIENTCHANGEPASS,
  },
  {
    Component: SessionCardP,
    path: PATIENTSPEECHLISTP,
  },
];
