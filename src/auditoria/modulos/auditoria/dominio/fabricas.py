from .entidades import Regulacion
from .excepciones import TipoObjetoNoExisteEnDominioAuditoriasExcepcion
from seedwork.dominio.repositorios import Mapeador
from seedwork.dominio.fabricas import Fabrica
from seedwork.dominio.entidades import Entidad
from seedwork.dominio.eventos import EventoDominio
from dataclasses import dataclass

@dataclass
class _FabricaRegulacion(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if not obj:
            return None 
        if isinstance(obj, list):
            return [self.crear_objeto(item, mapeador) for item in obj]
        if isinstance(obj, Entidad) or isinstance(obj, EventoDominio):
            return mapeador.entidad_a_dto(obj)
        else:            
            regulacion: Regulacion = mapeador.dto_a_entidad(obj)
            #self.validar_regla(MinimoUnRequisito(regulacion.requisitos)) Valoidar reglas  
            return regulacion

@dataclass
class FabricaAuditorias(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Regulacion.__class__:            
            fabrica_regulacion = _FabricaRegulacion()
            return fabrica_regulacion.crear_objeto(obj, mapeador)
        else:
            raise TipoObjetoNoExisteEnDominioAuditoriasExcepcion()

