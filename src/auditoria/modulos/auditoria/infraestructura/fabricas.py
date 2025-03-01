from dataclasses import dataclass, field
from seedwork.dominio.fabricas import Fabrica
from seedwork.dominio.repositorios import Repositorio
from seedwork.infraestructura.vistas import Vista
from modulos.auditoria.dominio.repositorios import RepositorioRegulaciones, RepositorioEventosRegulaciones
from .repositorios import RepositorioRegulacionesSQLAlchemy, RepositorioEventosRegulacionSQLAlchemy
from .excepciones import ExcepcionFabrica
from modulos.auditoria.dominio.entidades import Regulacion
from modulos.auditoria.infraestructura.vistas import VistaRegulacion

@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:        
        if obj == RepositorioRegulaciones:
            return RepositorioRegulacionesSQLAlchemy()
        elif obj == RepositorioEventosRegulaciones:            
            return RepositorioEventosRegulacionSQLAlchemy()
        else:
            raise ExcepcionFabrica(f'No existe fábrica para el objeto {obj}')
        
@dataclass
class FabricaVista(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Vista:
        if obj == Regulacion:
            return VistaRegulacion()
        else:
            raise ExcepcionFabrica(f'No existe fábrica para el objeto {obj}')