from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Iterable, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.modelos.conversacion import (
    Base,
    SesionConversacion,
    TurnoConversacion,
    calcular_duracion_segundos,
)


class ServicioConversaciones:
    """
    Servicio de alto nivel para registrar y consultar conversaciones.
    """

    def __init__(self, url_bd: str) -> None:
        self._engine = create_engine(url_bd, future=True)
        self._SessionLocal = sessionmaker(bind=self._engine, expire_on_commit=False)

        # Garantizamos que las tablas existan; en proyectos grandes se usaría Alembic.
        Base.metadata.create_all(self._engine)

    def crear_sesion(
        self, id_sesion: str, configuracion_usada: Optional[Dict[str, Any]] = None
    ) -> None:
        with self._SessionLocal() as sesion_bd:  # type: Session
            sesion = SesionConversacion(
                id_sesion=id_sesion, configuracion_usada=configuracion_usada
            )
            sesion_bd.add(sesion)
            sesion_bd.commit()

    def marcar_sesion_finalizada(self, id_sesion: str) -> None:
        with self._SessionLocal() as sesion_bd:
            sesion: Optional[SesionConversacion] = (
                sesion_bd.query(SesionConversacion)
                .filter(SesionConversacion.id_sesion == id_sesion)
                .first()
            )
            if not sesion:
                return
            sesion.fecha_fin = datetime.utcnow()
            sesion.duracion_segundos = calcular_duracion_segundos(
                sesion.fecha_inicio, sesion.fecha_fin
            )
            sesion_bd.commit()

    def guardar_turno(
        self,
        id_sesion: str,
        tipo_emisor: str,
        texto_transcrito: Optional[str] = None,
        longitud_tokens: Optional[int] = None,
    ) -> None:
        with self._SessionLocal() as sesion_bd:
            turno = TurnoConversacion(
                id_sesion=id_sesion,
                tipo_emisor=tipo_emisor,
                texto_transcrito=texto_transcrito,
                longitud_respuesta_tokens=longitud_tokens,
            )
            sesion_bd.add(turno)
            sesion_bd.commit()

    def obtener_conversacion(self, id_sesion: str) -> Optional[SesionConversacion]:
        with self._SessionLocal() as sesion_bd:
            sesion: Optional[SesionConversacion] = (
                sesion_bd.query(SesionConversacion)
                .filter(SesionConversacion.id_sesion == id_sesion)
                .first()
            )
            return sesion

    def iterar_turnos(self, id_sesion: str) -> Iterable[TurnoConversacion]:
        with self._SessionLocal() as sesion_bd:
            turnos = (
                sesion_bd.query(TurnoConversacion)
                .filter(TurnoConversacion.id_sesion == id_sesion)
                .order_by(TurnoConversacion.marca_tiempo.asc())
                .all()
            )
            for turno in turnos:
                yield turno


servicio_conversaciones: Optional[ServicioConversaciones] = None


def inicializar_servicio_conversaciones(url_bd: str) -> ServicioConversaciones:
    """
    Inicializa el servicio global de conversaciones.
    """

    global servicio_conversaciones
    if servicio_conversaciones is None:
        servicio_conversaciones = ServicioConversaciones(url_bd)
    return servicio_conversaciones

