import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControl,
  IconButton,
  InputAdornment,
  InputLabel,
  MenuItem,
  OutlinedInput,
  Select,
  useMediaQuery,
} from "@mui/material";
import { DatePicker } from "@mui/x-date-pickers";
import { useState } from "react";
import { Visibility, VisibilityOff } from "@mui/icons-material";
import dayjs from "dayjs";
import generatePassword from "omgopass";
import { doctor } from "..";
import { ShowErrorToastMessage, ShowInfoToastMessage } from "../utils/toasts";

//dialog function to add new patient
export const AddPatient = ({ open, handleClose }: any) => {
  const isMobile = useMediaQuery("(max-width:767px)");

  const [numberError, setNumberError] = useState<boolean>(true);
  const [showPassword, setShowPassword] = useState<any>(false);

  const [name, setName] = useState<string>("");
  const [date, setDate] = useState<dayjs.Dayjs | null>(null);
  const [pass, setPass] = useState<string>("");
  const [card, setCard] = useState<string>("");
  const [gender, setGender] = useState<string>("");

  const handleClickShowPassword = () => {
    setShowPassword((showPassword: any) => !showPassword);
  };
  const handleClick = async () => {
    console.log(card);
    const data = {
      full_name: name,
      date_of_birth: date && date.format("YYYY-MM-DD"),
      doctor_info: ["user1", "user2"],
      hospital: "Tomsk NII",
      gender: gender,
      card_number: card,
      constant_password: null,
      temporary_password: pass,
      is_password_changed: false,
      patient_info: "",
    };
    const cc = await doctor.createPatient(data);

    if (cc?.result_code === 1) {
      ShowErrorToastMessage(
        "Пользователь с таким номером карты уже существует"
      );
    } else {
      ShowInfoToastMessage("Пациент успешно добавлен!");
    }

    await handleClose();
  };

  const handleGeneratePassword = () => {
    const specchars = "!#$%&'()*+,-./:;<=>?@[]^_`{|}~";
    setPass(
      generatePassword({
        syllablesCount: 1,
        minSyllableLength: 7,
        maxSyllableLength: 7,
      }) + specchars[Math.floor(window.crypto.getRandomValues(new Uint32Array(1))[0] * 30)]
    );
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
      <DialogTitle>Добавить нового пациента</DialogTitle>
      <DialogContent>
        <div className="mt-4">
          <FormControl
            variant="outlined"
            className="mb-4"
            fullWidth
            required
            margin="normal"
          >
            <InputLabel>ФИО</InputLabel>
            <OutlinedInput
              value={name}
              style={{
                borderRadius: "15px",
                background: "#F8FAFC",
                width: isMobile ? "100%" : "",
              }}
              onChange={(e: any) => setName(e.target.value)}
              label="ФИО"
            />
          </FormControl>

          <FormControl
            variant="outlined"
            className="mb-4"
            fullWidth
            required
            error={numberError}
            margin="normal"
          >
            <InputLabel>Номер Карты</InputLabel>
            <OutlinedInput
              value={card}
              style={{
                borderRadius: "15px",
                background: "#F8FAFC",
                width: isMobile ? "100%" : "",
              }}
              onChange={(e: any) => {
                if (card.length === 11) {
                  setNumberError(false);
                } else {
                  setNumberError(true);
                }
                setCard(e.target.value);
              }}
              label="Номер Карты"
            />
          </FormControl>

          <div
            style={{
              margin: isMobile ? "10px 0" : "20px 0",
            }}
          >
            <DatePicker
              label="Дата рождения"
              sx={{ width: "100%" }}
              value={date}
              format="YYYY-MM-DD"
              onChange={(d: any) => setDate(d)}
            />
          </div>

          <FormControl variant="outlined" fullWidth margin="normal" required>
            <InputLabel>Пол</InputLabel>
            <Select
              onChange={(e: any) => {
                setGender(e.target.value);
              }}
              label="Пол"
              style={{
                borderRadius: "15px",
                background: "#F8FAFC",
                width: isMobile ? "100%" : "",
              }}
              value={gender}
            >
              <MenuItem value="m">Мужской</MenuItem>

              <MenuItem value="w">Женский</MenuItem>
            </Select>
          </FormControl>

          <FormControl variant="outlined" fullWidth margin="normal" required>
            <InputLabel>Пароль</InputLabel>
            <OutlinedInput
              style={{
                borderRadius: "15px",
                background: "#F8FAFC",
                width: isMobile ? "100%" : "",
              }}
              value={pass}
              onChange={(e: any) => setPass(e.target.value)}
              type={showPassword ? "text" : "password"}
              endAdornment={
                <InputAdornment position="end">
                  <IconButton onClick={handleClickShowPassword} edge="end">
                    {showPassword ? <VisibilityOff /> : <Visibility />}
                  </IconButton>
                </InputAdornment>
              }
              label="Password"
            />
          </FormControl>
        </div>
      </DialogContent>
      <DialogActions>
        <Button
          size="large"
          sx={{ px: 3, py: 1, borderRadius: "10px" }}
          variant="contained"
          onClick={handleGeneratePassword}
          disabled={pass != ""}
          style={{ marginRight: "40%" }}
        >
          Сгенерировать пароль
        </Button>
        <Button
          size="large"
          sx={{ px: 3, py: 1, borderRadius: "10px" }}
          onClick={handleClick}
          variant="contained"
          disabled={numberError}
        >
          Добавить
        </Button>
      </DialogActions>
    </Dialog>
  );
};
