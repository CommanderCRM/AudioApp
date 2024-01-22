import {
  Button,
  FormControl,
  IconButton,
  InputAdornment,
  InputLabel,
  OutlinedInput,
  useMediaQuery,
} from "@mui/material";
import { Visibility, VisibilityOff } from "@mui/icons-material";
import { useState } from "react";
import { client } from "../../..";
import { observer } from "mobx-react-lite";
import { useNavigate } from "react-router-dom";
import { PATIENTROOT } from "../../../utils/const";
import {
  ShowErrorToastMessage,
  ShowSuccessToastMessage,
} from "../../../utils/toasts";

//function returns change password page
export const ChangePassPage = observer(() => {
  const isMobile = useMediaQuery("(max-width:767px)");
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState<any>(false);

  const [newPass, setNewPass] = useState<any>("");

  const handleClick = async () => {
    const flag = await client.changeTempPass(newPass);

    if (flag === false) ShowErrorToastMessage("Ошибка, неверный пароль.");
    else ShowSuccessToastMessage("Успешно");

    if (flag) {
      navigate(PATIENTROOT);
    }
  };

  const handleClickShowPassword = () =>
    setShowPassword((showPassword: any) => !showPassword);

  return (
    <div className="flex flex-col justify-center w-80 mx-auto my-20">
      <FormControl
        required
        variant="outlined"
        fullWidth
        style={{
          marginBottom: isMobile ? "20px" : "40px",
        }}
      >
        <InputLabel>Старый Пароль</InputLabel>
        <OutlinedInput
          style={{
            borderRadius: "15px",
            background: "#F8FAFC",
            width: isMobile ? "100%" : "",
          }}
          value={client.lastPass}
          onChange={(e: any) => (client.lastPass = e.target.value)}
          type={showPassword ? "text" : "password"}
          endAdornment={
            <InputAdornment position="end">
              <IconButton onClick={handleClickShowPassword} edge="end">
                {showPassword ? <VisibilityOff /> : <Visibility />}
              </IconButton>
            </InputAdornment>
          }
          label="Старый Пароль"
        />
      </FormControl>
      <FormControl
        required
        variant="outlined"
        fullWidth
        style={{
          marginBottom: isMobile ? "20px" : "40px",
        }}
      >
        <InputLabel>Новый пароль</InputLabel>
        <OutlinedInput
          style={{
            borderRadius: "15px",
            background: "#F8FAFC",
            width: isMobile ? "100%" : "",
          }}
          value={newPass}
          onChange={(e: any) => setNewPass(e.target.value)}
          type={showPassword ? "text" : "password"}
          endAdornment={
            <InputAdornment position="end">
              <IconButton onClick={handleClickShowPassword} edge="end">
                {showPassword ? <VisibilityOff /> : <Visibility />}
              </IconButton>
            </InputAdornment>
          }
          label="Новый пароль"
        />
      </FormControl>

      <Button
        variant="contained"
        onClick={handleClick}
        disabled={
          client.card.length === 0 ||
          client.lastPass.length === 0 ||
          newPass.length === 0
        }
      >
        Сменить пароль
      </Button>
    </div>
  );
});
