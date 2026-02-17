import { useEffect, useRef, useState } from "react";

export interface EstadoAudioUsuario {
  nivelAudio: number;
  flujoAudio?: MediaStream;
}

/**
 * Hook que captura el micrófono y calcula un nivel de audio sencillo
 * para poder animar las barras de actividad.
 */
export function useAudioUsuario(activo: boolean): EstadoAudioUsuario {
  const [nivelAudio, setNivelAudio] = useState(0);
  const [flujoAudio, setFlujoAudio] = useState<MediaStream | undefined>();
  const analizadorRef = useRef<AnalyserNode | null>(null);

  useEffect(() => {
    if (!activo) {
      return;
    }

    let contextoAudio: AudioContext | null = null;
    let cancelar = false;

    async function inicializar() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        setFlujoAudio(stream);

        contextoAudio = new AudioContext();
        const fuente = contextoAudio.createMediaStreamSource(stream);
        const analizador = contextoAudio.createAnalyser();
        analizador.fftSize = 256;
        fuente.connect(analizador);
        analizadorRef.current = analizador;

        const datos = new Uint8Array(analizador.frequencyBinCount);

        function bucle() {
          if (cancelar || !analizadorRef.current) return;
          analizadorRef.current.getByteTimeDomainData(datos);
          let suma = 0;
          for (let i = 0; i < datos.length; i++) {
            const valor = datos[i] - 128;
            suma += Math.abs(valor);
          }
          const promedio = suma / datos.length;
          setNivelAudio(promedio / 128);
          requestAnimationFrame(bucle);
        }

        bucle();
      } catch (err) {
        console.error("Error al inicializar audio del usuario", err);
      }
    }

    inicializar();

    return () => {
      cancelar = true;
      if (contextoAudio) {
        contextoAudio.close();
      }
      if (flujoAudio) {
        flujoAudio.getTracks().forEach((t) => t.stop());
      }
    };
  }, [activo]);

  return { nivelAudio, flujoAudio };
}

