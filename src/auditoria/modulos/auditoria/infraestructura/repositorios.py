from config.db import db
from modulos.auditoria.dominio.repositorios import RepositorioEventosRegulaciones, RepositorioRegulaciones
from modulos.auditoria.dominio.entidades import Regulacion
from modulos.auditoria.dominio.fabricas import FabricaAuditorias
from .dto import Regulacion as RegulacionDTO
from .dto import EventosRegulacion
from .mapeadores import MapadeadorEventosRegulacion, MapeadorRegulacion
from uuid import UUID
from pulsar.schema import *


class RepositorioRegulacionesSQLAlchemy(RepositorioRegulaciones):

    def __init__(self):
        self._fabrica_auditorias: FabricaAuditorias = FabricaAuditorias()

    @property
    def fabrica_auditorias(self):
        return self._fabrica_auditorias

    def obtener_por_id(self, id: UUID) -> Regulacion:
        regulacion_dto = db.session.query(RegulacionDTO).filter_by(id=str(id)).one()
        return self._fabrica_auditorias.crear_objeto(regulacion_dto, MapeadorRegulacion())

    def obtener_todos(self) -> list[Regulacion]:
        # TODO
        raise NotImplementedError

    def agregar(self, regulacion: Regulacion):
        regulacion_dto = self.fabrica_auditorias.crear_objeto(regulacion, MapeadorRegulacion())
        db.session.add(regulacion_dto)

    def actualizar(self, regulacion: Regulacion):
        # TODO
        raise NotImplementedError

    def eliminar(self, regulacion_id: UUID):
        # TODO
        raise NotImplementedError

class RepositorioEventosRegulacionSQLAlchemy(RepositorioEventosRegulaciones):

    def __init__(self):
        self._fabrica_auditorias: FabricaAuditorias = FabricaAuditorias()

    @property
    def fabrica_auditorias(self):
        return self._fabrica_auditorias

    def obtener_por_id(self, id: UUID) -> Regulacion:
        regulacion_dto = db.session.query(RegulacionDTO).filter_by(id=str(id)).one()
        return self.fabrica_auditorias.crear_objeto(regulacion_dto, MapadeadorEventosRegulacion())

    def obtener_todos(self) -> list[Regulacion]:
        raise NotImplementedError

    def agregar(self, evento):
        regulacion_evento = self.fabrica_auditorias.crear_objeto(evento, MapadeadorEventosRegulacion())                
        parser_payload = JsonSchema(regulacion_evento.data.__class__)        
        json_str = parser_payload.encode(regulacion_evento.data)        
        evento_dto = EventosRegulacion()
        evento_dto.id = str(evento.id)
        evento_dto.id_entidad = str(evento.id_regulacion)
        evento_dto.fecha_evento = evento.fecha_creacion
        evento_dto.payload = str(regulacion_evento.specpayload)
        evento_dto.tipo_evento = evento.__class__.__name__
        evento_dto.formato_contenido = 'JSON'
        evento_dto.nombre_servicio = str(regulacion_evento.service_name)
        evento_dto.contenido = json_str
        db.session.add(evento_dto)

    def actualizar(self, regulacion: Regulacion):
        raise NotImplementedError

    def eliminar(self, regulacion_id: UUID):
        raise NotImplementedError
