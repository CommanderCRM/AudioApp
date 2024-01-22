import {
  Button,
  CircularProgress,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
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
import { client, doctor } from "../../..";
import { useParams } from "react-router-dom";
import { RecorderVoiceItem } from "../../../widgets/recordClient";

//function returns patient seans card page for client
export const SessionCardP = () => {
  const { patientID, session, type, flag } = useParams();
  const [sessionData, setSession] = useState(null);
  const [addPhrase, setAddPhrase] = useState<boolean>(false);

  const handleClose = () => {
    setAddPhrase(!addPhrase);
  };

  useEffect(() => {
    const promise = new Promise<any>((resolve) => {
      const res = client.getPatient();
      resolve(res);
    });
    promise.then((result) => {
      if (result.sessions) {
        const sess = result.sessions.find(
          (el: any) => el.session_id === Number(session)
        );
        setSession(sess);
      }
    });
  }, []);

  return (
    <>
      {addPhrase && (
        <PatientDialogExists
          card={patientID}
          open={addPhrase}
          handleClose={handleClose}
          session={session}
          sessiontype={type == "ф" ? "фразы" : "слоги"}
        />
      )}
      <div className="mx-10">
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

        <SessionTable session={sessionData} />
      </div>
    </>
  );
};

//function returns table with all seans phrases/syllables
const SessionTable = ({ session }: any) => {
  return !session ? (
    <div className="flex justify-center w-full">Сеансы отсутсвуют!</div>
  ) : (
    <>
      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }}>
          <TableHead>
            <TableRow>
              <TableCell>Индендефикатор</TableCell>
              <TableCell>Тип</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            <TableRow>
              <TableCell component="th" scope="row">
                {session.session_id}
              </TableCell>
              <TableCell>{session.session_type}</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </TableContainer>
    </>
  );
};

//dialog dunction to add phrases/syllables to the seans
const PatientDialogExists = ({
  open,
  handleClose,
  card,
  session,
  sessiontype,
}: any) => {
  console.log(session);
  const [step, setStep] = useState<any>(1);
  let key = "syllables";
  if (sessiontype == "фразы") {
    key = "phrases";
  }
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
                patientID={card}
                speechId={{
                  session_id: session,
                  session_type: sessiontype == "фразы" ? "фраз" : "слог",
                  sessionPatient: card,
                }}
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
