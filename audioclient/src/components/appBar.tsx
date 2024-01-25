import { AppBar, IconButton, Toolbar } from "@mui/material";
import LogoutIcon from "@mui/icons-material/Logout";
import { observer } from "mobx-react-lite";
import { client, doctor } from "..";
import { useNavigate } from "react-router-dom";

//function returns header component
export const AppBarComp = observer(({ name }: any) => {
  const navigate = useNavigate();
  const handelClick = () => {
    localStorage.clear();
    document.cookie = 'tok=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    doctor && doctor.clear();
    navigate("/");
  };
  if(!doctor.name && localStorage.getItem('tok')){
    doctor.name = localStorage.getItem('user');
    var role = localStorage.getItem('role')
    console.log(role == '1')
    doctor.specialist = role == '1';
  }
  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <span style={{ flexGrow: 1, fontSize: 30, fontWeight: 600 }}>
            {name}
          </span>
          <div className="flex justify-between items-center">
            <span style={{ marginRight: 10, fontSize: 20 }}>
              {name === "Доктор" || name === 'Специалист'
                ? doctor.name : client.card != ""  ? "№ " + client.card : client.card}
            </span>
            <IconButton color="inherit" onClick={handelClick}>
              <LogoutIcon />
            </IconButton>
          </div>
        </Toolbar>
      </AppBar>
    </>
  );
});
