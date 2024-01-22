import { Navigate, Route, Routes } from "react-router-dom";
import "./App.css";
import { MainURL } from "./utils/path";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

//main function
function App() {
  const renderRoutes = () => {
    return MainURL.map(({ path, Component }) => (
      <Route key={path} path={path} element={<Component />} />
    ));
  };

  return (
    <div className="App">
      <Routes>
        {renderRoutes()}
        <Route path="/error" element={<></>} />
        <Route path="*" element={<Navigate replace to="/" />} />
      </Routes>
      <ToastContainer />
    </div>
  );
}

export default App;
