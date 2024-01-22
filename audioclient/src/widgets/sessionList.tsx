import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControl,
  IconButton,
  InputLabel,
  MenuItem,
  Select,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@mui/material";
import Paper from "@mui/material/Paper";
import { useNavigate, useParams } from "react-router-dom";
import { DOCTORROOT, PATIENTROOT } from "../utils/const";
import CompareArrowsIcon from "@mui/icons-material/CompareArrows";
import { useState } from "react";
import { doctor } from "..";
import {
  ShowSuccessToastMessage,
  ShowWarningToastMessage,
} from "../utils/toasts";
import { DialogProcess } from "./DialogProcess";

//fucntion returns seans table
export const SessionList = ({ speechList, name }: any) => {
  const { patientID } = useParams();
  const navigate = useNavigate();
  const [isOpen, setIsOpen] = useState<any>();

  const handleClick = (sessionID: any, sessionType: any, flag: any) => {
    if (name === "doctor") {
      navigate(
        DOCTORROOT +
          "/card/" +
          patientID +
          "/" +
          sessionType[0] +
          "/" +
          Number(flag) +
          "/" +
          sessionID
      );
    }
  };

  const handleCompare = (e: any) => {
    e.stopPropagation();
    handleClose();
  };

  const handleClose = () => {
    setIsOpen(!isOpen);
  };

  return (
    <>
      {isOpen && (
        <DialogComponent
          open={isOpen}
          handleClose={handleClose}
          speechList={speechList}
          patientID={patientID}
        />
      )}
      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }}>
          <TableHead>
            <TableRow>
              <TableCell>Индентификатор сессии</TableCell>
              <TableCell>Тип сигнала</TableCell>
              <TableCell>Тип сеанса</TableCell>
              <TableCell></TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {speechList.map((row: any) => (
              <TableRow
                key={row.session_id}
                style={{ cursor: "pointer" }}
                onClick={() =>
                  handleClick(
                    row.session_id,
                    row.session_type,
                    row.is_reference_session
                  )
                }
              >
                <TableCell>{row.session_id}</TableCell>
                <TableCell>
                  {row.is_reference_session ? "Эталонная" : "Неэталлоная"}
                </TableCell>
                <TableCell>{row.session_type}</TableCell>
                <TableCell align="right">
                  {row.session_type === "слоги" && name == "doctor" ? (
                    <IconButton onClick={handleCompare}>
                      <CompareArrowsIcon />
                    </IconButton>
                  ) : (
                    <></>
                  )}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </>
  );
};

//dialog functions to compare seanses
const DialogComponent = ({ open, handleClose, speechList, patientID }: any) => {
  const [first, setFirst] = useState<any>();

  const [second, setSecond] = useState(speechList[0]?.session_id || "");

  const [open1, setOpen1] = useState<any>(false);
  const [isSave, setSave] = useState<any>(true);

  const handleEstimate = async () => {
    const data = {
      sessions_id: [first, second],
    };

    setOpen1(true);
    ShowSuccessToastMessage("Проверка  займет некоторое время");

    const res = await doctor.estimatePhrase(patientID, data);

    setSave(false);
  };

  return (
    <>
      <DialogProcess
        open={open1}
        handleClose={() => setOpen1(!open)}
        isSave={isSave}
      />
      <Dialog open={open} onClose={handleClose} fullWidth>
        <DialogTitle>Выбрать 1-2 сеансы для сравнения</DialogTitle>
        <DialogContent>
          <FormControl variant="outlined" fullWidth margin="normal" required>
            <InputLabel>Эталонный сеанс</InputLabel>
            <Select
              value={first}
              onChange={(e: any) => {
                setFirst(e.target.value);
              }}
              label="Эталонный сеанс"
            >
              {speechList.map(
                (row: any) =>
                  row.session_type === "слоги" &&
                  row.is_reference_session && (
                    <MenuItem value={row.session_id}>{row.session_id}</MenuItem>
                  )
              )}
            </Select>
          </FormControl>
          <FormControl variant="outlined" fullWidth margin="normal" required>
            <InputLabel>Не эталонный сеанс</InputLabel>
            <Select
              value={second}
              onChange={(e: any) => {
                setSecond(e.target.value);
              }}
              label="Не эталонный сеанс"
            >
              {speechList.map(
                (row: any) =>
                  row.session_type === "слоги" &&
                  !row.is_reference_session && (
                    <MenuItem value={row.session_id}>{row.session_id}</MenuItem>
                  )
              )}
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button
            size="large"
            sx={{ px: 3, py: 1, borderRadius: "10px" }}
            variant="contained"
            onClick={handleEstimate}
            style={{ marginRight: "40%" }}
          >
            Сравнить
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
};
