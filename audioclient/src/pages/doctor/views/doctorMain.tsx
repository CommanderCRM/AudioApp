import React, { useEffect, useState } from "react";
import {
  Button,
  CircularProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  TextField,
} from "@mui/material";
import { AddPatient } from "../../../widgets/patientForm";
import { useNavigate } from "react-router";
import { doctor } from "../../..";
import { observer } from "mobx-react-lite";

interface Patient {
  card_number: number;
  full_name: string;
  date_of_birth: string;
  gender: string;
  doctor_info: string[];
}

interface DockerTableProps {
  searchTerm: string;
  setFilteredRows: React.Dispatch<React.SetStateAction<Patient[]>>;
}

//function returns table with all doctor's patients
const DockerTable: React.FC<DockerTableProps> = observer(
  ({ searchTerm, setFilteredRows }) => {
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [rows, setRows] = useState<Patient[]>([]);

    useEffect(() => {
      const fetchData = async () => {
        setIsLoading(true);
        const data = await doctor.getPatients();
        setRows(data);
        setIsLoading(false);
      };

      fetchData();
    }, [doctor.isUpdatePatient]);

    useEffect(() => {
      let filtered = rows.filter((row) =>
        row.full_name.toLowerCase().includes(searchTerm.toLowerCase())
      );
      if (filtered.length == 0) {
        filtered = rows.filter((row) =>
          row.card_number.toString().includes(searchTerm.toLowerCase())
        );
      }
      setFilteredRows(filtered);
    }, [searchTerm, rows, setFilteredRows]);

    return isLoading ? (
      <div className="flex justify-center w-full">
        <CircularProgress />
      </div>
    ) : (
      <></>
    );
  }
);

interface TableItemProps {
  data: Patient[];
}

// fucntion returns table rows with patient's info
const TableItem: React.FC<TableItemProps> = ({ data }) => {
  const navigate = useNavigate();

  return data.length === 0 ? (
    <div className="flex justify-center w-full">Пациенты отсутствуют</div>
  ) : (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }}>
        <TableHead>
          <TableRow>
            <TableCell sx={{ fontSize: 16, fontWeight: 600 }}>
              Полное имя
            </TableCell>
            <TableCell align="right" sx={{ fontSize: 16, fontWeight: 600 }}>
              Возраст
            </TableCell>
            <TableCell align="right" sx={{ fontSize: 16, fontWeight: 600 }}>
              Пол
            </TableCell>
            <TableCell align="right" sx={{ fontSize: 16, fontWeight: 600 }}>
              Номер личной карты
            </TableCell>
            <TableCell align="right" sx={{ fontSize: 16, fontWeight: 600 }}>
              Информация
            </TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {data.map((row) => (
            <TableRow
              key={row.card_number}
              style={{ cursor: "pointer" }}
              onClick={() => navigate("/doctor/card/" + row.card_number)}
            >
              <TableCell component="th" scope="row">
                {row.full_name}
              </TableCell>
              <TableCell align="right">{row.date_of_birth}</TableCell>
              <TableCell align="right">
                {row.gender === "m" ? "Мужской" : "Женский"}
              </TableCell>
              <TableCell align="right">{row.card_number}</TableCell>
              <TableCell align="right">
                {row.doctor_info.map((item) => (
                  <span key={item}>{item} </span>
                ))}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

//function returns doctor's main page
export const DoctorMainPage: React.FC = () => {
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [searchTerm, setSearchTerm] = useState<string>("");
  const [filteredRows, setFilteredRows] = useState<Patient[]>([]);

  const handleClose = () => {
    doctor.isUpdatePatient = !doctor.isUpdatePatient;
    setIsOpen(!isOpen);
  };
  console.log(doctor)
  return (
    <>
      {isOpen && <AddPatient open={isOpen} handleClose={handleClose} />}
      {
        
        !doctor.specialist ? <div className="flex w-full justify-end my-10 pe-5">
        <Button
          variant="contained"
          onClick={handleClose}
          size="large"
          sx={{ px: 3, py: 1, borderRadius: "10px" }}
        >
          Добавить пациента
        </Button>
      </div> : ''}
      

      <div>
        <TextField
          label="Поиск пациента"
          variant="outlined"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          style={doctor.specialist? {marginTop:100} : {}}
          sx={{ mb: 2, mx: 2 }}
        />
      </div>
      <DockerTable searchTerm={searchTerm} setFilteredRows={setFilteredRows} />
      <TableItem data={filteredRows} />
    </>
  );
};
