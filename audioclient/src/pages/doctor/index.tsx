import { Routes, Route, Navigate } from "react-router-dom";
import { DoctorURL } from "../../utils/path";
import { AppBarComp } from "../../components/appBar";
import { doctor } from "../..";

//function renders all doctor's routes
export const DoctorRoot = () => {
  const renderRoutes = () => {
    return DoctorURL.map(({ path, Component }) => (
      <Route key={path} path={path} element={<Component />} />
    ));
  };
  var role = localStorage.getItem('role')
  console.log(role == '1')
  doctor.specialist = role == '1';
  const title = doctor.specialist ? 'Специалист':'Доктор';
  return (
    <>
      <AppBarComp name={title} />
      <Routes>
        {renderRoutes()}
        <Route path="/error" element={<></>} />
        <Route path="*" element={<Navigate replace to="/" />} />
      </Routes>
    </>
  );
};
