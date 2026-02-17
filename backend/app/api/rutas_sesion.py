import uuid
from fastapi import APIRouter

from app.core.configuracion import configuracion
from app.modelos.mensajes_voz import (
    PeticionIniciarSesion,
    RespuestaIniciarSesion,
)
from app.servicios.servicio_conversaciones import inicializar_servicio_conversaciones
from app.servicios.servicio_gemini_live import servicio_gemini_live


router = APIRouter(prefix="/sesion", tags=["sesion"])

# Almacén en memoria de sesiones Live activas.
sesiones_activas = {}


@router.post("", response_model=RespuestaIniciarSesion)
async def iniciar_sesion(peticion: PeticionIniciarSesion) -> RespuestaIniciarSesion:
    """
    Crea una nueva sesión de conversación y devuelve el identificador y la URL
    del WebSocket que debe usar el frontend.
    """

    id_sesion = str(uuid.uuid4())

    # Creamos la sesión Live de Gemini y la guardamos en memoria.
    sesion_live = servicio_gemini_live.crear_sesion()
    sesiones_activas[id_sesion] = sesion_live

    # Registramos la sesión en la base de datos.
    servicio_conv = inicializar_servicio_conversaciones(configuracion.db_url)
    configuracion_usada = {
        "modelo": configuracion.gemini_modelo,
        "max_tokens_respuesta": configuracion.asistente_max_tokens_respuesta,
        "temperatura": configuracion.asistente_temperatura,
        "prompt_sistema": configuracion.asistente_prompt_sistema,
        "usuario_id": peticion.usuario_id,
    }
    servicio_conv.crear_sesion(id_sesion=id_sesion, configuracion_usada=configuracion_usada)

    url_ws = "/voz"

    return RespuestaIniciarSesion(id_sesion=id_sesion, url_websocket=url_ws)

