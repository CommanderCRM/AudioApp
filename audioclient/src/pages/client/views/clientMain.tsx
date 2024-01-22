import {
  CircularProgress,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
} from "@mui/material";
import { FC, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { client } from "../../..";
import { AppBarComp } from "../../../components/appBar";
import { PATIENTROOT } from "../../../utils/const";
import { observer } from "mobx-react-lite";

interface Doctor {
  doctor_name: string;
  doctor_specialization: string;
}

//function returns patient main page
export const ClientMain = () => {
  const [searchTerm, setSearchTerm] = useState<string>("");
  return (
    <div
      style={{ display: "flex", flexDirection: "column", alignItems: "center" }}
    >
      <AppBarComp name="Пациент" />

      <div className="font-bold my-5 mx-2" style={{ fontSize: "28px" }}>
        Ваши врачи
      </div>
      <div style={{ marginRight: "12%", width: "50%" }}>
        <TextField
          label="Поиск врача"
          variant="outlined"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          sx={{ mb: 2, mx: 2 }}
        />
      </div>
      <DoctorsTable searchTerm={searchTerm} />
    </div>
  );
};

interface DockerTableProps {
  searchTerm: string;
}

//functions returns table with all patient's doctors
const DoctorsTable: FC<DockerTableProps> = ({ searchTerm }) => {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [filteredRows, setFilteredRows] = useState<Doctor[]>([]);
  const [data, setData] = useState<Doctor[]>([]);

  useEffect(() => {
    (async () => {
      setIsLoading(true);
      const d1 = await client.getDoctors();
      setData(d1);
      setIsLoading(false);
    })();
  }, []);

  useEffect(() => {
    let filtered = data.filter((row) =>
      row.doctor_name.toLowerCase().includes(searchTerm.toLowerCase())
    );
    setFilteredRows(filtered);
  }, [searchTerm, data]);

  return isLoading ? (
    <div className="flex justify-center w-full">
      <CircularProgress />
    </div>
  ) : data.length === 0 ? (
    <div className="flex justify-center w-full">
      Врачи отсутсвуют! Обратитесь в больницу для записи к врачу.
    </div>
  ) : (
    <div className="flex justify-center w-full">
      <TableItem data={filteredRows} />
    </div>
  );
};

//function returns a table row with doctor's info
const TableItem = observer((data: any) => {
  const handleClick = (row: any, index: any) => {
    navigate(PATIENTROOT + "/card/" + index);
    client.doctorId = index;
  };

  const navigate = useNavigate();
  return (
    <TableContainer
      component={Paper}
      sx={{
        borderRadius: 0,
        maxWidth: "60%",
      }}
    >
      <Table>
        <TableHead>
          <TableRow>
            <TableCell sx={{ fontSize: 16, fontWeight: 600 }}>ФИО</TableCell>
            <TableCell sx={{ fontSize: 16, fontWeight: 600 }}>
              Специализация
            </TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {data.data.map((row: any, index: any) => (
            <TableRow
              key={row.doctor_name}
              style={{ cursor: "pointer" }}
              onClick={() => handleClick(row, index)}
            >
              <TableCell component="th" scope="row">
                {row.doctor_name}
              </TableCell>
              <TableCell>{row.doctor_specialization}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
});
