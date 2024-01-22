import axios from "axios";
import { makeAutoObservable } from "mobx";
import { $api_doctor } from "../utils/api_doctor";

//class describe all doctor's functions
export default class Doctor {
  name: any = "";
  isUpdatePatient: boolean = false;

  constructor() {
    makeAutoObservable(this);
  }
  //add patient
  async createPatient(form: any) {
    try {
      const res = await $api_doctor.post("/patients/", form, {
        headers: { "Content-Type": "application/json" },
      });

      return res.data;
    } catch (err: any) {
      return err.response.data;
    }
  }
  //login
  async login(username: string, password: string) {
    this.name = username;
    try {
      const response = await axios.post(
        `${process.env.REACT_APP_BASE_URL_DOCTOR}login/`,
        { username, password },
        { withCredentials: true }
      );
      if(response.data.access_token){
        localStorage.setItem("tok", response.data.access_token);
        let date = new Date();
      date.setTime(date.getTime() + 24 * 60 * 60 * 1000);

      document.cookie = `tok=${
        response.data.refresh_token
      }; path=/;expires=${date.toUTCString()}`;
      return true;
      }else {
        return false;
      }



    } catch (err) {
      return false;
    }
  }
  //get doctor's patients
  async getPatients() {
    try {
      const response = await $api_doctor.get(`patients`, {
        params: { limit: 100 },
      });

      return response.data;
    } catch (err) {
      return [];
    }
  }
  //get patient's info
  async getPatient(number: number) {
    try {
      const response = await $api_doctor.get(`patients/${number}`);

      return response.data;
    } catch (err) {
      return {};
    }
  }

  //get seans info
  async getPatientSessionInfo(patientID: any, session: any) {
    try {
      const response = await $api_doctor.get(
        `patients/${patientID}/session/${session}`
      );

      return response.data;
    } catch (err) {
      console.log(err);
      return {};
    }
  }
  //create new seans
  async createScenario(
    card: any,
    is_reference_session: any,
    session_type: any
  ) {
    try {
      const response = await $api_doctor.post(`patients/${card}`, {
        is_reference_session,
        session_type,
        session_info: "",
      });
      return response.data;
    } catch (err) {
      return {};
    }
  }
  //add speech to seans
  async updateSessionSpeech(speechId: any, data: any) {
    console.log(speechId);
    try {
      const response = await $api_doctor.post(
        `patients/${speechId.sessionPatient}/speech/${speechId.session_id}`,
        data
      );
      return response.data;
    } catch (err) {
      return {};
    }
  }
  //get all phrases
  async getExampleSpeech(patientID: any, speechId: any) {
    try {
      const response = await $api_doctor.get(
        `patients/${patientID}/session/${speechId}/speech`
      );

      return response.data;
    } catch (err) {
      return {};
    }
  }

  //get definite phase/syllable
  async getSpeech(session: any, speechId: any, phrase: any) {
    try {
      // const response = await $api_doctor.get(`patients/${session}/session/${speechId}/speech`)
      const response = await $api_doctor.get(
        `patients/${session}/session/${speechId}/speech/${phrase}`
      );

      return response.data;
    } catch (err) {
      return {};
    }
  }

  //add audio to seans
  async estimateSpeech(patientID: any, session: any) {
    try {
      // const response = await $api_doctor.get(`patients/${session}/session/${speechId}/speech`)
      const response = await $api_doctor.patch(
        `patients/${patientID}/session/${session}`,
        { card_number: patientID, session_id: Number(session) }
      );

      return response.data;
    } catch (err) {
      return {};
    }
  }

  //update phrase
  async estimatePhrase(patientID: any, data: any) {
    try {
      const response = await $api_doctor.patch(
        `patients/${patientID}/session`,
        data
      );
    } catch (err) {}
  }
}
