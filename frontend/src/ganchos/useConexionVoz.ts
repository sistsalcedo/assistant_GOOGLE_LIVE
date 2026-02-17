import { useEffect, useRef, useState } from "react";

export type EstadoSesionVoz =
  | "sinSesion"
  | "creandoSesion"
  | "conectando"
  | "enConversacion"
  | "finalizada";

export interface EstadoConexionVoz {
  estadoSesion: EstadoSesionVoz;
  estaHablandoUsuario: boolean;
  estaHablandoAgente: boolean;
  nivelAudioAgente: number;
}

/**
 * Hook responsable de gestionar el WebSocket con el backend.
 * Aquí solo se implementa el esqueleto básico; el audio del agente
 * se deja como futuro trabajo según el formato exacto que exponga Gemini.
 */
export function useConexionVoz(
  urlWebSocketRelativa: string | null,
  idSesion: string | null,
  flujoAudioUsuario?: MediaStream
): EstadoConexionVoz {
  const [estadoSesion, setEstadoSesion] = useState<EstadoSesionVoz>("sinSesion");
  const [estaHablandoUsuario, setEstaHablandoUsuario] = useState(false);
  const [estaHablandoAgente, setEstaHablandoAgente] = useState(false);
  const [nivelAudioAgente, setNivelAudioAgente] = useState(0);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (!urlWebSocketRelativa || !idSesion) {
      return;
    }

    setEstadoSesion("conectando");

    const url = new URL(urlWebSocketRelativa, window.location.origin.replace(/^http/, "ws"));
    url.searchParams.set("id_sesion", idSesion);

    const ws = new WebSocket(url.toString());
    wsRef.current = ws;

    ws.onopen = () => {
      setEstadoSesion("enConversacion");
    };

    ws.onmessage = (event) => {
      if (typeof event.data === "string") {
        try {
          const json = JSON.parse(event.data);
          if (json.tipo === "evento") {
            switch (json.nombre_evento) {
              case "inicio_respuesta_agente":
                setEstaHablandoAgente(true);
                break;
              case "fin_respuesta_agente":
                setEstaHablandoAgente(false);
                break;
              case "sesion_finalizada":
                setEstadoSesion("finalizada");
                ws.close();
                break;
              default:
                break;
            }
          }
        } catch {
          // ignoramos mensajes de texto no estructurados
        }
      } else {
        // Aquí se podría procesar el audio binario del agente
        // y calcular nivelAudioAgente.
        setNivelAudioAgente(0.5);
      }
    };

    ws.onclose = () => {
      setEstadoSesion((prev) => (prev === "finalizada" ? prev : "finalizada"));
    };

    ws.onerror = () => {
      setEstadoSesion("finalizada");
    };

    return () => {
      ws.close();
    };
  }, [urlWebSocketRelativa, idSesion]);

  // Por simplicidad aún no se envía el audio del usuario; eso requerirá
  // codificar el stream de MediaStream a chunks binarios (por ejemplo WebRTC,
  // Web Audio API + encoder). El esqueleto de estado ya está preparado.

  useEffect(() => {
    if (flujoAudioUsuario) {
      setEstaHablandoUsuario(true);
    } else {
      setEstaHablandoUsuario(false);
    }
  }, [flujoAudioUsuario]);

  return {
    estadoSesion,
    estaHablandoUsuario,
    estaHablandoAgente,
    nivelAudioAgente
  };
}

