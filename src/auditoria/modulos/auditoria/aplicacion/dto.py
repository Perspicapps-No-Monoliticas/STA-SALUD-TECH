from dataclasses import dataclass, field
from seedwork.aplicacion.dto import DTO

 
@dataclass(frozen=True)
class RegulacionDTO(DTO):
    id: str = field(default_factory=str)
    nombre: str = field(default_factory=str)
    region: str = field(default_factory=str)
    payload: str = field(default_factory=str)
    fecha_actualizacion: str = field(default_factory=str)
    fecha_creacion: str = field(default_factory=str)