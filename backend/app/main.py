from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import rutas_sesion, rutas_voz


def crear_aplicacion() -> FastAPI:
    """
    Crea y configura la instancia principal de FastAPI.
    """

    app = FastAPI(title="Chat de voz con Gemini 2.5 Flash")

    # Configuración CORS básica para permitir al frontend acceder al backend.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(rutas_sesion.router)
    app.include_router(rutas_voz.router)

    return app


app = crear_aplicacion()

