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
import { client, doctor } from "../../..";
import { RecorderVoiceItem } from "../../../widgets/recordClient";
import { AppBarComp } from "../../../components/appBar";
import { observer } from "mobx-react-lite";
import { SessionList } from "../../../widgets/sessionList";

//function returns patient's doctor's page with seanses
export const DoctorCardPage = observer(() => {
  const [isOpen, setIsOpen] = useState<any>(false);
  const [speechList, setSpeechList] = useState<any>([]);

  useEffect(() => {
    (async () => {
      const res = await client.getPatient();
      if (res) {
        setSpeechList(res.sessions);
      }
    })();
  }, []);

  const handleClose = () => setIsOpen(!isOpen);

  return (
    <>
      <AppBarComp name="Пациент" />

      {isOpen && (
        <PatientDialog
          card={client.card}
          open={isOpen}
          handleClose={handleClose}
        />
      )}
      <div className="px-5">
        <span style={{ fontSize: "36px", fontWeight: 600 }} className="my-5">
          Информация о враче
        </span>
        <ProfileCard />

        <div className="flex justify-between w-full my-5">
          <span className="text-2xl">Сеансы оценки качества речи</span>
          <Button
            variant="contained"
            onClick={handleClose}
            size="large"
            sx={{ px: 3, py: 1, borderRadius: "10px" }}
          >
            Добавить сеанс
          </Button>
        </div>
        <div className="flex justify-between w-full gap-x-5 mt-5">
          {speechList.length ? (
            <SessionList speechList={speechList} name="patient" />
          ) : (
            <span style={{ fontSize: 16 }}>Сеансы отсутсвуют</span>
          )}
        </div>
      </div>
    </>
  );
});

//function returns doctor's profile card
const ProfileCard = observer(() => {
  const [doctor, setDoctor] = useState({
    doctor_name: "",
    doctor_specialization: "",
  });
  useEffect(() => {
    (async () => {
      const res: any = await client.getDoctors();

      setDoctor(res[client.doctorId]);
    })();
  }, []);
  return (
    <div
      className="p-10"
      style={{
        maxWidth: "300px",
        border: "1px solid silver",
        borderRadius: "8px",
      }}
    >
      <div style={{ marginBottom: 10 }}>
        <span>
          <b>ФИО: </b>
        </span>
        <span>{doctor.doctor_name}</span>
      </div>
      <div>
        <span>
          <b>Специализация: </b>
        </span>
        <span>{doctor.doctor_specialization}</span>
      </div>
    </div>
  );
});

//dialog function to add seans with doctor
const PatientDialog = ({ open, handleClose, card }: any) => {
  const [step, setStep] = useState<any>(0);
  const [is_reference_session, setIsRef] = useState(0);
  const [session_type, setSessionType] = useState("фразы");
  const [speech, setSpeech] = useState<any>({});

  const handleButtonNext = async () => {
    if (step === 0) {
      const sp = await client.createSession(session_type);
      setSpeech({
        sessionId: sp,
        session_type: session_type,
        sessionPatient: card,
      });
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
                session_type={session_type}
                is_reference_session={is_reference_session}
              />
            </>
          ) : step === 1 ? (
            <>
              <RecorderVoiceItem
                speechId={speech}
                handleButtonNext={handleButtonNext}
                patientID={client.card}
              />
            </>
          ) : (
            <>Вы записали все фразы</>
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
  session_type,
  is_reference_session,
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
          defaultValue={is_reference_session}
        >
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
          <MenuItem value="фразы">Фразы</MenuItem>
          <MenuItem value="слоги">Слоги</MenuItem>
        </Select>
      </FormControl>
    </>
  );
};
const steps = ["Добавление сеанса", "Загрузка аудио", "Завершение"];
