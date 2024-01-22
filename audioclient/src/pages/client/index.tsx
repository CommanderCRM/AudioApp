import { Routes, Route, Navigate } from "react-router-dom";
import { PatientURL } from "../../utils/path";

// function renders patient routes
export const PatientRoot = () => {
  const renderRoutes = () => {
    return PatientURL.map(({ path, Component }) => (
      <Route key={path} path={path} element={<Component />} />
    ));
  };

  return (
    <>
      <Routes>
        {renderRoutes()}
        <Route path="/error" element={<></>} />
        <Route path="*" element={<Navigate replace to="/" />} />
      </Routes>
    </>
  );
};
