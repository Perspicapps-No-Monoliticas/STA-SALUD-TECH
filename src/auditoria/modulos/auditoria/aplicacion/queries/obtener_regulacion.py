from seedwork.aplicacion.queries import Query, QueryResultado
from seedwork.aplicacion.queries import ejecutar_query as query
from modulos.auditoria.dominio.entidades import Regulacion
from dataclasses import dataclass
from .base import RegulacionQueryBaseHandler
from modulos.auditoria.aplicacion.mapeadores import MapeadorRegulacion

@dataclass
class ObtenerRegulacion(Query):
    id: str

class ObtenerRegulacionHandler(RegulacionQueryBaseHandler):

    def handle(self, query: ObtenerRegulacion) -> QueryResultado:
        vista = self.fabrica_vista.crear_objeto(Regulacion)
        result = vista.obtener_por(id=query.id)
        regulacion =  self.fabrica_auditorias.crear_objeto(result, MapeadorRegulacion())
        return QueryResultado(resultado=regulacion)

@query.register(ObtenerRegulacion)
def ejecutar_query_obtener_reserva(query: ObtenerRegulacion):
    handler = ObtenerRegulacionHandler()
    return handler.handle(query)