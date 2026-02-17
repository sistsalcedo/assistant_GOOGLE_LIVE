from datetime import datetime
from typing import Optional

from sqlalchemy import JSON, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class SesionConversacion(Base):
    """
    Representa una sesión de conversación de voz entre un usuario y el agente.
    """

    __tablename__ = "sesiones"

    id_sesion = Column(String, primary_key=True, index=True)
    fecha_inicio = Column(DateTime, default=datetime.utcnow, nullable=False)
    fecha_fin = Column(DateTime, nullable=True)
    duracion_segundos = Column(Float, nullable=True)
    configuracion_usada = Column(JSON, nullable=True)

    turnos = relationship("TurnoConversacion", back_populates="sesion", cascade="all, delete-orphan")


class TurnoConversacion(Base):
    """
    Un turno dentro de una sesión: puede ser del usuario o del agente.
    """

    __tablename__ = "turnos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_sesion = Column(String, ForeignKey("sesiones.id_sesion"), nullable=False, index=True)
    tipo_emisor = Column(String, nullable=False)  # "usuario" o "agente"
    marca_tiempo = Column(DateTime, default=datetime.utcnow, nullable=False)
    texto_transcrito = Column(String, nullable=True)
    longitud_respuesta_tokens = Column(Integer, nullable=True)

    sesion = relationship("SesionConversacion", back_populates="turnos")


def calcular_duracion_segundos(
    fecha_inicio: datetime, fecha_fin: Optional[datetime]
) -> Optional[float]:
    """
    Utilidad para calcular la duración de una sesión en segundos.
    """

    if not fecha_fin:
        return None
    return (fecha_fin - fecha_inicio).total_seconds()

