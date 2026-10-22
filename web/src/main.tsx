import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.tsx";
import "./styles/App.css";
import { applyTheme, loadTheme } from "./theme";

applyTheme(loadTheme());

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
