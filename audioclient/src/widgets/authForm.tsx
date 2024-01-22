import { Visibility, VisibilityOff } from "@mui/icons-material";
import {
  FormControl,
  IconButton,
  InputAdornment,
  InputLabel,
  OutlinedInput,
  useMediaQuery,
} from "@mui/material";
import { useState } from "react";

//fucntion returns common auth fields
export const AuthFields = ({
  name,
  username,
  password,
  setUserName,
  setPassword,
}: any) => {
  const [showPassword, setShowPassword] = useState<any>(false);
  const isMobile = useMediaQuery("(max-width:767px)");

  const handleClickShowPassword = () =>
    setShowPassword((showPassword: any) => !showPassword);

  return (
    <>
      <span className="AuthTitle  my-20">Вход {name}а</span>
      {name === "Врач" ? (
        <DoctorForm
          username={username}
          password={password}
          setUserName={setUserName}
          setPassword={setPassword}
        />
      ) : (
        <ClientForm username={username} setUserName={setUserName} />
      )}

      <FormControl
        required
        variant="outlined"
        fullWidth
        style={{
          marginBottom: isMobile ? "20px" : "40px",
        }}
      >
        <InputLabel>Пароль</InputLabel>
        <OutlinedInput
          style={{
            borderRadius: "15px",
            background: "#F8FAFC",
            width: isMobile ? "100%" : "",
          }}
          value={password}
          onChange={(e: any) => setPassword(e.target.value)}
          type={showPassword ? "text" : "password"}
          endAdornment={
            <InputAdornment position="end">
              <IconButton onClick={handleClickShowPassword} edge="end">
                {showPassword ? <VisibilityOff /> : <Visibility />}
              </IconButton>
            </InputAdornment>
          }
          label="Пароль"
        />
      </FormControl>
    </>
  );
};

//fucntion returns doctor's auth fields
const DoctorForm = ({ username, password, setUserName, setPassword }: any) => {
  const isMobile = useMediaQuery("(max-width:767px)");

  return (
    <>
      <FormControl
        style={{
          marginBottom: isMobile ? "20px" : "40px",
        }}
        variant="outlined"
        fullWidth
        required
      >
        <InputLabel>Логин</InputLabel>
        <OutlinedInput
          style={{
            borderRadius: "15px",
            background: "#F8FAFC",
            width: isMobile ? "100%" : "",
          }}
          type="email"
          onChange={(e: any) => setUserName(e.target.value)}
          value={username}
          label="Логин"
        />
      </FormControl>
    </>
  );
};

////fucntion returns patient's auth fields
const ClientForm = ({ username, setUserName }: any) => {
  const isMobile = useMediaQuery("(max-width:767px)");
  return (
    <>
      <FormControl
        style={{
          marginBottom: isMobile ? "20px" : "40px",
        }}
        variant="outlined"
        fullWidth
        required
        error={username.length !== 12 || !/^\d+$/.test(username)}
      >
        <InputLabel>Номер Карты</InputLabel>
        <OutlinedInput
          style={{
            borderRadius: "15px",
            background: "#F8FAFC",
            width: isMobile ? "100%" : "",
          }}
          type="email"
          onChange={(e: any) => setUserName(e.target.value)}
          value={username}
          label="Номер Карты"
        />
      </FormControl>
    </>
  );
};
