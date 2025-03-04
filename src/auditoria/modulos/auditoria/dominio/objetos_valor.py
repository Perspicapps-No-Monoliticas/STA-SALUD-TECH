from __future__ import annotations

from dataclasses import dataclass, field
from seedwork.dominio.objetos_valor import ObjetoValor

@dataclass(frozen=True)
class Nombre():
    nombre: str

@dataclass(frozen=True)
class Region():
    nombre: str

@dataclass(frozen=True)
class Payload():
    nombre: str    