import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Step,
  StepLabel,
  Stepper,
} from "@mui/material";
import { useEffect, useState } from "react";

import { useParams } from "react-router-dom";
import { doctor } from "../../..";
import { SessionList } from "../../../widgets/sessionList";

import { RecorderVoiceItem } from "../../../widgets/recordDoc";
import { PhraseChart } from "../../../widgets/phraseChart";
import { SlogChart } from "../../../widgets/slogChart";

//function returns page with all patient's seanses for doctor
export const PatientCardPage = () => {
  const [patient, setPatient] = useState<any>();
  const [speechList, setSpeechList] = useState<any>([]);
  const [openChartPhrases, setOpenChartPrases] = useState<boolean>(false);
  const [openChartSlog, setOpenChartSlog] = useState<boolean>(false);
  const { patientID } = useParams();

  useEffect(() => {
    (async () => {
      const res = await doctor.getPatient(Number(patientID));
      if (res) {
        setPatient(res.get_patient_info);
        setSpeechList(res.sessions);
      }
    })();
  }, []);

  const [isOpen, setIsOpen] = useState<boolean>(false);

  const handleClose = () => {
    setIsOpen(!isOpen);
  };
  const handleSlog = () => {
    setOpenChartSlog(true);
  };
  const handlePhrases = () => {
    setOpenChartPrases(true);
  };
  const handleCloseChart = () => {
    setOpenChartPrases(false);
    setOpenChartSlog(false);
  };

  return (
    <>
      {openChartPhrases && (
        <PhraseChart
          handleCloseChart={handleCloseChart}
          open={openChartPhrases}
          sessionsData={speechList}
        />
      )}
      {openChartSlog && (
        <SlogChart
          handleCloseChart={handleCloseChart}
          open={openChartSlog}
          sessionsData={speechList}
        />
      )}
      {isOpen && (
        <PatientDialog
          card={patientID}
          open={isOpen}
          handleClose={handleClose}
        />
      )}
      <div className="px-5">
        <div style={{ fontSize: "36px" }} className="my-5 font-bold">
          Профиль пациента
        </div>
        <div className="flex flex-wrap justify-between">
          <ProfileCard patient={patient} />
        </div>
        <div className="flex justify-between w-full my-5">
          <div style={{ fontSize: "24px" }}>Сеансы оценки качества речи</div>
          <Button
            variant="contained"
            onClick={handlePhrases}
            size="large"
            sx={{ px: 3, py: 1, borderRadius: "10px" }}
          >
            График фраз
          </Button>
          <Button
            variant="contained"
            onClick={handleSlog}
            size="large"
            sx={{ px: 3, py: 1, borderRadius: "10px" }}
          >
            График слогов
          </Button>
          <Button
            variant="contained"
            onClick={handleClose}
            size="large"
            sx={{ px: 3, py: 1, borderRadius: "10px" }}
          >
            Добавить сеанс
          </Button>
        </div>
        {speechList?.length ? (
          <SessionList speechList={speechList} name="doctor" />
        ) : (
          <span style={{ fontSize: 16 }}>Сеансы отсутсвуют</span>
        )}
      </div>
    </>
  );
};

//function returns patient's profile card
const ProfileCard = ({ patient }: any) => {
  return (
    <div
      className="p-10"
      style={{
        maxWidth: "450px",
        minHeight: "30%",
        border: "1px solid silver",
        borderRadius: "8px",
        padding: "3%",
      }}
    >
      {patient &&
        Object.entries(patient).map(([key, val]: any) => (
          <div key={key} style={{ marginBottom: 10 }}>
            <span style={{ fontSize: 16 }} className="font-bold">
              <b>{data[key]}: </b>
            </span>
            <span style={{ paddingLeft: 5 }}>
              {key === "gender" ? (val === "m" ? "мужчина" : "женщина") : val}
            </span>
            <br />
          </div>
        ))}
    </div>
  );
};

const data: any = {
  full_name: "Имя",
  date_of_birth: "Возраст",
  gender: "Пол",
  card_number: "Персональный номер карты",
  doctor_info: "Дополнительная информация",
  patient_info: "Информация о пациенте",
};

//dialog function to add new seans with patient
const PatientDialog = ({ open, handleClose, card }: any) => {
  const [step, setStep] = useState<any>(0);

  const [is_reference_session, setIsRef] = useState(1);
  const [session_type, setSessionType] = useState("фраз");
  const [speech, setSpeech] = useState<any>(null);

  const handleButtonNext = async () => {
    if (step === 0) {
      const sp = await doctor.createScenario(
        card,
        is_reference_session,
        session_type === "фраз" ? session_type + "ы" : session_type + "и"
      );
      setSpeech({ ...sp, session_type: session_type, sessionPatient: card });
    }

    setStep(step + 1);

    if (step === 2) {
      setStep(0);
      handleClose();
    }
  };

  return (
    <>
      <Dialog open={open} onClose={handleClose} fullWidth>
        <DialogTitle>
          <Stepper activeStep={step}>
            {steps.map((label) => (
              <Step key={label}>
                <StepLabel>{label}</StepLabel>
              </Step>
            ))}
          </Stepper>
        </DialogTitle>
        <DialogContent>
          {step === 0 ? (
            <>
              <IputType
                setIsRef={setIsRef}
                setSessionType={setSessionType}
                is_reference_session={is_reference_session}
                session_type={session_type}
              />
            </>
          ) : step === 1 ? (
            <>
              <RecorderVoiceItem
                speechId={speech}
                phrasesold={[]}
                handleButtonNext={handleButtonNext}
              />
            </>
          ) : (
            <>Вы записали все речи</>
          )}
        </DialogContent>
        <DialogActions>
          {step === 0 ? (
            <Button onClick={handleButtonNext} variant="contained">
              Вперед
            </Button>
          ) : (
            <Button onClick={handleButtonNext} variant="contained">
              Завершить
            </Button>
          )}
        </DialogActions>
      </Dialog>
    </>
  );
};

//function returns the seans type input fields to the dialog
const IputType = ({
  setIsRef,
  setSessionType,
  is_reference_session,
  session_type,
}: any) => {
  return (
    <>
      <FormControl variant="outlined" fullWidth margin="normal" required>
        <InputLabel>Тип сеанса</InputLabel>
        <Select
          value={is_reference_session}
          onChange={(e: any) => {
            setIsRef(e.target.value);
          }}
          label="Тип сигнала"
        >
          <MenuItem value={1}>Эталонный</MenuItem>

          <MenuItem value={0}>Не эталонный</MenuItem>
        </Select>
      </FormControl>
      <FormControl variant="outlined" fullWidth margin="normal" required>
        <InputLabel>Тип сигнала</InputLabel>
        <Select
          value={session_type}
          onChange={(e: any) => {
            setSessionType(e.target.value);
          }}
          label="Тип сигнала"
        >
          <MenuItem value="фраз">Фраза</MenuItem>
          <MenuItem value="слог">Слог</MenuItem>
        </Select>
      </FormControl>
    </>
  );
};

const steps = ["Добавление сеанса", "Загрузка аудио", "Завершение"];
