from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Dict, Optional

from google import genai
from google.genai import types as genai_types

from app.core.configuracion import configuracion


class SesionGeminiLive:
    """
    Envoltura de alto nivel sobre una sesión Live de Gemini.
    """

    def __init__(
        self,
        cliente: genai.Client,
        modelo: str,
        configuracion_asistente: Dict[str, Any],
    ) -> None:
        self._cliente = cliente
        self._modelo = modelo
        self._configuracion_asistente = configuracion_asistente
        self._sesion: Optional[genai.LiveSession] = None
        self._lock = asyncio.Lock()

    @asynccontextmanager
    async def conectar(self) -> AsyncGenerator["SesionGeminiLive", None]:
        """
        Abre la conexión Live y la cierra automáticamente al salir del contexto.
        """

        async with self._lock:
            if self._sesion is None:
                live_config = genai_types.LiveConnectConfig(
                    response_modalities=["AUDIO"],
                    speech_config=genai_types.SpeechConfig(
                        voice_config=genai_types.VoiceConfig(
                            prebuilt_voice_config=genai_types.PrebuiltVoiceConfig(
                                voice_name="Charon"  # nombre de voz de ejemplo
                            )
                        )
                    ),
                    generation_config=genai_types.GenerationConfig(
                        max_output_tokens=self._configuracion_asistente[
                            "max_tokens_respuesta"
                        ],
                        temperature=self._configuracion_asistente["temperatura"],
                    ),
                    system_instruction=self._configuracion_asistente["prompt_sistema"],
                )
                self._sesion = await self._cliente.aio.live.connect(
                    model=self._modelo,
                    config=live_config,
                )
        try:
            yield self
        finally:
            await self.cerrar()

    async def enviar_audio_usuario(self, datos_audio: bytes, fin_de_turno: bool) -> None:
        """
        Envía audio del usuario a la sesión Live.
        """

        if not self._sesion:
            raise RuntimeError("La sesión Live de Gemini no está inicializada.")

        await self._sesion.send(
            genai_types.LiveClientEvent(
                realtime_input=genai_types.Content(
                    role="user",
                    parts=[
                        genai_types.Blob(
                            mime_type="audio/pcm", data=datos_audio  # formato de ejemplo
                        )
                    ],
                ),
                # `turn_complete` indica que el usuario ha terminado de hablar.
                turn_complete=fin_de_turno,
            )
        )

    async def iterar_respuestas_agente(self) -> AsyncGenerator[genai_types.Message, None]:
        """
        Itera sobre los mensajes que Gemini envía de vuelta.
        """

        if not self._sesion:
            raise RuntimeError("La sesión Live de Gemini no está inicializada.")

        async for respuesta in self._sesion.receive():
            yield respuesta

    async def cerrar(self) -> None:
        """
        Cierra la sesión Live si está abierta.
        """

        if self._sesion is not None:
            await self._sesion.close()
            self._sesion = None


class ServicioGeminiLive:
    """
    Servicio singleton que gestiona el cliente de Gemini y crea sesiones Live.
    """

    def __init__(self) -> None:
        self._cliente = genai.Client(api_key=configuracion.gemini_api_key)
        self._modelo = configuracion.gemini_modelo

    def crear_sesion(self) -> SesionGeminiLive:
        """
        Crea una nueva sesión Live con la configuración actual del asistente.
        """

        configuracion_asistente = {
            "max_tokens_respuesta": configuracion.asistente_max_tokens_respuesta,
            "temperatura": configuracion.asistente_temperatura,
            "prompt_sistema": configuracion.asistente_prompt_sistema,
        }
        return SesionGeminiLive(
            cliente=self._cliente,
            modelo=self._modelo,
            configuracion_asistente=configuracion_asistente,
        )


servicio_gemini_live = ServicioGeminiLive()

