import React, { useState } from "react";
import { iniciarSesion } from "../servicios/clienteApi";
import { useAudioUsuario } from "../ganchos/useAudioUsuario";
import { useConexionVoz } from "../ganchos/useConexionVoz";
import { PanelCanal } from "../componentes/PanelCanal";

export const PaginaAtencion: React.FC = () => {
  const [idSesion, setIdSesion] = useState<string | null>(null);
  const [urlWebSocket, setUrlWebSocket] = useState<string | null>(null);
  const [iniciando, setIniciando] = useState(false);

  const audioUsuario = useAudioUsuario(Boolean(idSesion));
  const conexionVoz = useConexionVoz(urlWebSocket, idSesion, audioUsuario.flujoAudio);

  const puedeIniciar =
    conexionVoz.estadoSesion === "sinSesion" || conexionVoz.estadoSesion === "finalizada";

  const manejarIniciar = async () => {
    try {
      setIniciando(true);
      const respuesta = await iniciarSesion();
      setIdSesion(respuesta.id_sesion);
      setUrlWebSocket("/api" + respuesta.url_websocket);
    } catch (error) {
      console.error(error);
      alert("No se pudo iniciar la atención. Revisa el backend.");
    } finally {
      setIniciando(false);
    }
  };

  const manejarFinalizar = () => {
    // De momento confiamos en que cerrar la pestaña o recargar
    // cerrará la sesión; para un flujo completo habría que enviar
    // un comando \"finalizar_sesion\" por el WebSocket.
    setIdSesion(null);
    setUrlWebSocket(null);
  };

  return (
    <main className="min-h-screen flex flex-col items-center justify-center px-4">
      <section className="w-full max-w-2xl space-y-8">
        <header className="space-y-2 text-center">
          <h1 className="text-2xl font-semibold tracking-tight">
            Atención por voz con asistente IA
          </h1>
          <p className="text-sm text-slate-400">
            Pulsa &quot;Iniciar atención&quot; para comenzar una conversación de voz con el
            agente. Este diseño está inspirado en PersonaPlex, con canales separados para
            el usuario y el asistente.
          </p>
        </header>

        <div className="space-y-4">
          <PanelCanal
            titulo="Agente"
            descripcion="Respuestas del asistente IA"
            estaHablando={conexionVoz.estaHablandoAgente}
            nivelAudio={conexionVoz.nivelAudioAgente}
          />
          <PanelCanal
            titulo="Usuario"
            descripcion="Tu voz (micrófono)"
            estaHablando={conexionVoz.estaHablandoUsuario}
            nivelAudio={audioUsuario.nivelAudio}
          />
        </div>

        <div className="flex justify-center gap-4">
          <button
            type="button"
            disabled={!puedeIniciar || iniciando}
            onClick={manejarIniciar}
            className="px-6 py-2 rounded-full bg-emerald-500 text-slate-950 font-semibold disabled:opacity-50"
          >
            {iniciando ? "Iniciando..." : "Iniciar atención"}
          </button>
          <button
            type="button"
            disabled={!idSesion}
            onClick={manejarFinalizar}
            className="px-6 py-2 rounded-full border border-slate-600 text-slate-200 disabled:opacity-40"
          >
            Finalizar sesión
          </button>
        </div>
      </section>
    </main>
  );
};

