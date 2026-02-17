from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings


class ConfiguracionAplicacion(BaseSettings):
    """
    Configuración principal de la aplicación leída desde variables de entorno.

    Todos los nombres de campos están en español para mantener coherencia
    con el resto del código.
    """

    gemini_api_key: str = Field(..., alias="GEMINI_API_KEY")
    gemini_modelo: str = Field(..., alias="GEMINI_MODELO")

    backend_host: str = Field("0.0.0.0", alias="BACKEND_HOST")
    backend_puerto: int = Field(8000, alias="BACKEND_PORT")

    db_url: str = Field("sqlite:///./datos_conversaciones.db", alias="DB_URL")

    asistente_max_tokens_respuesta: int = Field(
        256, alias="ASISTENTE_MAX_TOKENS_RESPUESTA"
    )
    asistente_temperatura: float = Field(0.7, alias="ASISTENTE_TEMPERATURA")
    asistente_prompt_sistema: str = Field(
        "Eres un asistente amable que responde de forma breve y clara.",
        alias="ASISTENTE_PROMPT_SISTEMA",
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        populate_by_name = True


@lru_cache()
def obtener_configuracion() -> ConfiguracionAplicacion:
    """
    Devuelve una instancia cacheada de la configuración de la aplicación.

    Se usa `lru_cache` para evitar recrear el objeto en cada importación.
    """

    return ConfiguracionAplicacion()


configuracion = obtener_configuracion()

