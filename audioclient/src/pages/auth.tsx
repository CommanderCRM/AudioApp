import { Button, Tab, Tabs } from "@mui/material";
import { useState } from "react";
import { AuthFields } from "../widgets/authForm";
import { client, doctor } from "..";
import { useNavigate } from "react-router-dom";
import { PATIENTCHANGEPASS, DOCTORROOT, PATIENTROOT } from "../utils/const";
import { observer } from "mobx-react-lite";
import {
  ShowErrorToastMessage,
  ShowSuccessToastMessage,
} from "../utils/toasts";

//function returns authorization page(both for doctor and patient)
export const AuthPage = observer(() => {
  const navigate = useNavigate();

  const [nav, setNav] = useState<string>("Пациент");
  const [username, setUserName] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [disabled, setDisabled] = useState<boolean>(false);

  const handleClick = async () => {
    setDisabled(true);
    if (username.length !== 0 && password.length !== 0) {
      let flag = false;
      if (nav === "Врач") {
        flag = await doctor.login(username, password);
        if (flag) {
          ShowSuccessToastMessage("Выполнено успешно!");
          navigate(DOCTORROOT);
        } else {
          ShowErrorToastMessage("Неверный логин или пароль!");
        }
      } else {
        if (nav === 'Специалист'){
          flag = await doctor.login(username, password);
          
        if (flag) {
          ShowSuccessToastMessage("Выполнено успешно!");
          navigate(DOCTORROOT);
        } else {
          ShowErrorToastMessage("Неверный логин или пароль!");
        }
        }
        client.card = username;
        client.lastPass = password;
        flag = await client.checkStatusPass();
        if (flag === false) {
          navigate(PATIENTROOT + "/" + PATIENTCHANGEPASS);
        } else if (flag === true) {
          const flag = await client.login(username, password);
          if (flag === false) {
            ShowErrorToastMessage("Неверный логин или пароль!");
          } else {
            navigate(PATIENTROOT);
            ShowSuccessToastMessage("Выполнено успешно!");
          }
        }
      }
    }
    setDisabled(false);
  };

  const handleChange = (event: any, newVal: any) => setNav(newVal);

  return (
    <div className="flex flex-col justify-center w-80 mx-auto my-10">
      <Tabs onChange={handleChange} value={nav} centered>
        <Tab label="Пациент" value="Пациент" />
        <Tab label="Врач / Специалист" value="Врач" />
        {/* <Tab label="Специалист" value="Специалист" /> */}
      </Tabs>

      <AuthFields
        name={nav}
        username={username}
        password={password}
        setUserName={setUserName}
        setPassword={setPassword}
      />

      <Button variant="contained" onClick={handleClick} disabled={disabled}>
        Войти
      </Button>
    </div>
  );
});
