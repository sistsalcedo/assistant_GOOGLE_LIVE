import asyncio
from typing import Dict

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.core.configuracion import configuracion
from app.modelos.mensajes_voz import MensajeWebSocketServidor
from app.servicios.servicio_conversaciones import inicializar_servicio_conversaciones
from app.servicios.servicio_gemini_live import SesionGeminiLive
from app.api.rutas_sesion import sesiones_activas


router = APIRouter(tags=["voz"])


async def _enviar_evento(
    websocket: WebSocket, nombre_evento: str, detalle: str | None = None
) -> None:
    mensaje = MensajeWebSocketServidor(nombre_evento=nombre_evento, detalle=detalle)
    await websocket.send_json(mensaje.model_dump())


@router.websocket("/voz")
async def websocket_voz(websocket: WebSocket, id_sesion: str) -> None:
    """
    WebSocket principal que conecta el navegador con la sesión Live de Gemini.
    """

    await websocket.accept()

    if id_sesion not in sesiones_activas:
        await _enviar_evento(
            websocket,
            nombre_evento="error",
            detalle="Sesión no encontrada o expirada.",
        )
        await websocket.close()
        return

    sesion_live: SesionGeminiLive = sesiones_activas[id_sesion]

    servicio_conv = inicializar_servicio_conversaciones(configuracion.db_url)

    # Timeout de inactividad en segundos.
    timeout_inactividad = 60 * 5

    async def recibir_audio_desde_cliente() -> None:
        ultimo_mensaje = asyncio.get_event_loop().time()
        try:
            async with sesion_live.conectar():
                while True:
                    try:
                        mensaje = await asyncio.wait_for(
                            websocket.receive_bytes(), timeout=timeout_inactividad
                        )
                        ultimo_mensaje = asyncio.get_event_loop().time()
                        # Por ahora asumimos que todo mensaje binario es audio del usuario
                        # y que el cliente usará un mensaje JSON separado para fin_de_turno
                        await sesion_live.enviar_audio_usuario(
                            datos_audio=mensaje, fin_de_turno=False
                        )
                        servicio_conv.guardar_turno(
                            id_sesion=id_sesion,
                            tipo_emisor="usuario",
                            texto_transcrito=None,
                        )
                    except asyncio.TimeoutError:
                        await _enviar_evento(
                            websocket,
                            nombre_evento="sesion_finalizada",
                            detalle="Sesión cerrada por inactividad.",
                        )
                        break
        except WebSocketDisconnect:
            pass
        finally:
            servicio_conv.marcar_sesion_finalizada(id_sesion)
            sesiones_activas.pop(id_sesion, None)
            await sesion_live.cerrar()

    async def enviar_respuestas_a_cliente() -> None:
        try:
            async with sesion_live.conectar():
                async for respuesta in sesion_live.iterar_respuestas_agente():
                    # Aquí deberíamos inspeccionar el tipo de mensaje; por ahora
                    # asumimos que contiene audio binario listo para el cliente.
                    # En una implementación real habría que extraer los bytes.
                    await _enviar_evento(
                        websocket,
                        nombre_evento="inicio_respuesta_agente",
                        detalle=None,
                    )
                    # Esto es un marcador de posición; en la práctica se enviaría audio.
                    await websocket.send_bytes(b"")  # audio del agente
                    await _enviar_evento(
                        websocket,
                        nombre_evento="fin_respuesta_agente",
                        detalle=None,
                    )
        except WebSocketDisconnect:
            pass

    # Ejecutamos ambas corrutinas en paralelo.
    await asyncio.gather(recibir_audio_desde_cliente(), enviar_respuestas_a_cliente())

