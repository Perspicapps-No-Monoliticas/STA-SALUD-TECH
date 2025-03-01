from __future__ import annotations
from dataclasses import dataclass, field
import datetime

import modulos.auditoria.dominio.objetos_valor as ov
from modulos.auditoria.dominio.eventos import RegulacionCreada
from seedwork.dominio.entidades import AgregacionRaiz

@dataclass
class Regulacion(AgregacionRaiz):    
    nombre: ov.Nombre = field(default=ov.Nombre)    
    region: ov.Region = field(default=ov.Region)
    payload: ov.Payload = field(default=ov.Payload)
    requisitos: list[ov.Requisito] = field(default_factory=list[ov.Requisito])

    def crear_regulacion(self, regulacion: Regulacion):        
        self.nombre = regulacion.nombre
        self.region = regulacion.region
        self.payload = regulacion.payload
        self.requisitos = regulacion.requisitos
        self.fecha_creacion = datetime.datetime.now()

        self.agregar_evento(RegulacionCreada(id_regulacion=self.id, nombre=self.nombre, region=self.region, payload = self.payload,
                                              requisitos=self.requisitos, fecha_creacion=self.fecha_creacion))
        # TODO Agregar evento de compensación
