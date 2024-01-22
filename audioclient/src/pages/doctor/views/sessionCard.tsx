import {
  Button,
  CircularProgress,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  IconButton,
  Step,
  StepLabel,
  Stepper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@mui/material";
import { useEffect, useState } from "react";
import Paper from "@mui/material/Paper";
import { doctor } from "../../..";
import { useParams } from "react-router-dom";
import PlayCircleOutlineIcon from "@mui/icons-material/PlayCircleOutline";
import FileDownloadIcon from "@mui/icons-material/FileDownload";
import {
  ShowErrorToastMessage,
  ShowSuccessToastMessage,
} from "../../../utils/toasts";
import { RecorderVoiceItem } from "../../../widgets/recordDoc";
import { DialogProcess } from "../../../widgets/DialogProcess";

//function returns patient's seans page for doctor
export const SessionCard = () => {
  const { patientID, session, type, flag } = useParams();
  const [values, setValues] = useState([]);
  const [reload, setReload] = useState<boolean>(false);
  const [addPhrase, setAddPhrase] = useState<boolean>(false);
  const [open, setOpen] = useState<any>(false);
  const [isSave, setIsSave] = useState<boolean>(true);

  useEffect(() => {
    const promise = new Promise<any>((resolve) => {
      const res = doctor.getPatientSessionInfo(patientID, session);
      resolve(res);
    });
    promise.then((result) => {
      if (result.speech_array) {
        const vals = result.speech_array.map((el: any) => {
          return el.real_value;
        });
        setValues(vals);
      }
    });
  }, []);

  const handleClose = () => {
    setAddPhrase(!addPhrase);
    setReload(true);
  };
  const handleEstimate = async () => {
    setOpen(true);
    ShowSuccessToastMessage("Оценка займет некоторое время");
    const res = await doctor.estimateSpeech(patientID, session);

    if (res && Object.keys(res).length === 0) {
      ShowErrorToastMessage("Произошла ошибка при обработке");
    } else {
      setIsSave(false);
    }
    setIsSave(false);
  };
  return (
    <div className="mx-10">
      <DialogProcess
        open={open}
        handleClose={() => setOpen(!open)}
        isSave={isSave}
      />
      {addPhrase && (
        <PatientDialogExists
          card={patientID}
          open={addPhrase}
          handleClose={handleClose}
          session={session}
          sessiontype={type == "ф" ? "фразы" : "слоги"}
          values={values}
        />
      )}
      <div style={{ color: "#1976d2" }} className="my-5">
        Индендефикатор сеанса: {session}
      </div>
      <div
        className="flex justify-between my-5"
        style={{ alignItems: "center" }}
      >
        <div>
          <div style={{ fontSize: "36px" }} className="font-bold">
            Тип биологического сигнала: {type == "ф" ? "фраза" : "слог"}
          </div>
          <div style={{ fontSize: 18, padding: "5px 10px" }}>
            Тип сеанса: {flag === "1" ? "Эталонный" : "Неэталонный"}
          </div>
        </div>
        {type === "ф" && (
          <div>
            <Button
              variant="contained"
              onClick={handleEstimate}
              size="large"
              sx={{ px: 3, py: 1, borderRadius: "10px", marginRight: "10px" }}
            >
              Оценить
            </Button>
          </div>
        )}
        <div>
          <Button
            variant="contained"
            size="large"
            onClick={handleClose}
            sx={{ px: 3, py: 1, borderRadius: "10px" }}
          >
            Добавить фразы
          </Button>
        </div>
      </div>

      <SessionTable reload={reload} setReload={setReload} />
    </div>
  );
};

//fucntion returns the table with all session phrases/syllables
const SessionTable = ({ reload, setReload }: any) => {
  const [data, setData] = useState({ speech_array: [] });
  const [isLoading, setisLoading] = useState(false);
  const { patientID, session } = useParams();
  const [audioSrc, setAudioSrc] = useState("");
  const [isPlaying, setIsPlaying] = useState(false);

  useEffect(() => {
    (async () => {
      setisLoading(true);
      const d1 = await doctor.getPatientSessionInfo(patientID, session);
      setData(d1);
      setisLoading(false);
    })();
    setReload(false);
  }, [reload]);

  const handleDownload = async (phrase: any) => {
    const res = await doctor.getSpeech(patientID, session, phrase);

    const blob = new Blob(
      [
        new Uint8Array(
          atob(res.base64_value)
            .split("")
            .map((c) => c.charCodeAt(0))
        ),
      ],
      {
        type: "audio/wav",
      }
    );

    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `audio_${phrase}.wav`;

    a.click();

    URL.revokeObjectURL(url);
    a.remove();
  };

  const handlePlay = async (phrase: any) => {
    const res = await doctor.getSpeech(patientID, session, phrase);

    setAudioSrc("data:audio/wav;base64," + res.base64_value);
    setIsPlaying(true);
  };
  return isLoading ? (
    <div className="flex justify-center w-full">
      <CircularProgress />
    </div>
  ) : Object.keys(data).length === 0 ? (
    <div className="flex justify-center w-full">Сеансы отсутсвуют!</div>
  ) : (
    <>
      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }}>
          <TableHead>
            <TableRow>
              <TableCell>Индендефикатор</TableCell>
              <TableCell>Реальная значение</TableCell>
              <TableCell>Тип</TableCell>
              <TableCell></TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.speech_array.map((row: any) => (
              <TableRow key={row.signal_id} style={{ cursor: "pointer" }}>
                <TableCell component="th" scope="row">
                  {row.signal_id}
                </TableCell>
                <TableCell>{row.real_value}</TableCell>
                <TableCell>{row.signal_type}</TableCell>
                <TableCell align="right">
                  <IconButton onClick={() => handlePlay(row.signal_id)}>
                    <PlayCircleOutlineIcon />
                  </IconButton>
                  <IconButton onClick={() => handleDownload(row.signal_id)}>
                    <FileDownloadIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      {isPlaying && (
        <audio autoPlay onEnded={() => setIsPlaying(false)} src={audioSrc}>
          Your browser does not support the audio element.
        </audio>
      )}
    </>
  );
};

//dialog function to add phrases/syllable to seans
const PatientDialogExists = ({
  open,
  handleClose,
  card,
  session,
  sessiontype,
  values,
}: any) => {
  const [prevSess, setPrevSess] = useState<any>(null);
  const [step, setStep] = useState<any>(1);
  let key = "syllables";
  if (sessiontype == "фразы") {
    key = "phrases";
  }
  useEffect(() => {
    const promise = new Promise<any>((resolve) => {
      const res = doctor.getExampleSpeech(card, session);
      resolve(res);
    });
    promise.then((result) => {
      if (result[key]) {
        const phrases = result[key].filter((el: any) => !values.includes(el));
        setPrevSess(phrases);
        if (phrases.length == 0) {
          handleButtonNext();
        }
      }
    });
  }, []);

  const handleButtonNext = () => {
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
          {step === 1 ? (
            <>
              <RecorderVoiceItem
                speechId={{
                  session_id: session,
                  session_type: sessiontype == "фразы" ? "фраз" : "слог",
                  sessionPatient: card,
                }}
                phrasesold={prevSess}
                handleButtonNext={handleButtonNext}
              />
            </>
          ) : (
            <>Вы записали все речи</>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleButtonNext} variant="contained">
            Завершить
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

const steps = ["Добавление сеанса", "Загрузка аудио", "Завершение"];
