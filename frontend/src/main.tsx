import React from "react";
import ReactDOM from "react-dom/client";
import { PaginaAtencion } from "./paginas/PaginaAtencion";
import "./estilos.css";

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <PaginaAtencion />
  </React.StrictMode>
);

