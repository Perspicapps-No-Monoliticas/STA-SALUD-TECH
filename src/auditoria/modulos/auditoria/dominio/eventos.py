from __future__ import annotations
from dataclasses import dataclass, field
from seedwork.dominio.eventos import (EventoDominio)
import modulos.auditoria.dominio.objetos_valor as ov
from datetime import datetime

class EventoRegulacion(EventoDominio):
    ...

@dataclass
class RegulacionCreada(EventoRegulacion):
    id_regulacion: uuid.UUID = None
    nombre: str = None
    payload: str = None
    region: str = None
    fecha_creacion: datetime = None