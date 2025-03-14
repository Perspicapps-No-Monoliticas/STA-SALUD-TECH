from seedwork.aplicacion.queries import QueryHandler
from modulos.auditoria.infraestructura.fabricas import FabricaVista
from modulos.auditoria.dominio.fabricas import FabricaAuditorias

class RegulacionQueryBaseHandler(QueryHandler):
    def __init__(self):
        self._fabrica_vista: FabricaVista = FabricaVista()
        self._fabrica_auditorias: FabricaAuditorias = FabricaAuditorias()

    @property
    def fabrica_vista(self):
        return self._fabrica_vista
    
    @property
    def fabrica_auditorias(self):
        return self._fabrica_auditorias    