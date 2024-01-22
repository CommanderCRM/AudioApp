import React, { createContext } from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import { BrowserRouter } from "react-router-dom";
import { LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import Doctor from "./store/doctor";
import Client from "./store/client";

//main layout

interface StateDoctor {
  doctor: Doctor;
}

interface StateClient {}

export const doctor = new Doctor();

export const client = new Client();

export const Context = createContext<StateDoctor>({
  doctor,
});

export const ContextClient = createContext<StateClient>({
  client,
});

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <Context.Provider value={{ doctor }}>
        <ContextClient.Provider value={{ client }}>
          <LocalizationProvider dateAdapter={AdapterDayjs}>
            <App />
          </LocalizationProvider>
        </ContextClient.Provider>
      </Context.Provider>
    </BrowserRouter>
  </React.StrictMode>
);
