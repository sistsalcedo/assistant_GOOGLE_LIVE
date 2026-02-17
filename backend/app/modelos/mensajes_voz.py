from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel


class PeticionIniciarSesion(BaseModel):
    """
    Cuerpo de la petición para iniciar una nueva sesión de atención.
    """

    # En el futuro se puede añadir más metadatos del usuario.
    usuario_id: Optional[str] = None


class RespuestaIniciarSesion(BaseModel):
    """
    Respuesta que el backend devuelve al frontend al iniciar una sesión.
    """

    id_sesion: str
    url_websocket: str


class MensajeWebSocketCliente(BaseModel):
    """
    Mensaje estructurado que el cliente puede enviar por el WebSocket.

    El audio en sí viajará típicamente como binario separado, pero este
    modelo sirve para comandos de control.
    """

    tipo: Literal["comando"] = "comando"
    accion: Literal["fin_turno", "finalizar_sesion", "ping"] = "fin_turno"
    marca_tiempo: datetime = datetime.utcnow()


class MensajeWebSocketServidor(BaseModel):
    """
    Mensaje estructurado que el servidor puede enviar al cliente.
    """

    tipo: Literal["evento"] = "evento"
    nombre_evento: Literal[
        "inicio_respuesta_agente",
        "fin_respuesta_agente",
        "interrupcion_detectada",
        "sesion_finalizada",
        "error",
    ]
    detalle: Optional[str] = None

