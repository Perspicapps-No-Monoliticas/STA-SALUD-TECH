from seedwork.aplicacion.comandos import Comando
from modulos.auditoria.aplicacion.dto import RegulacionDTO
from .base import CrearRegulacionBaseHandler
from dataclasses import dataclass, field
from seedwork.aplicacion.comandos import ejecutar_commando as comando

from modulos.auditoria.dominio.entidades import Regulacion
from seedwork.infraestructura.uow import UnidadTrabajoPuerto
from modulos.auditoria.aplicacion.mapeadores import MapeadorRegulacion
from modulos.auditoria.infraestructura.repositorios import RepositorioRegulaciones, RepositorioEventosRegulaciones

#UN CommanHandler se usa para ejecutar el comando en este caso CrearRegulacion es el comando y CrearRegulacionaHandler es el handler quien ejecuta al comando
@dataclass
class CrearRegulacion(Comando): #ESTE ES EL COMANDO
    id: str
    nombre: str
    region: str    
    payload: str 
    fecha_actualizacion: str 


class CrearRegulacionHandler(CrearRegulacionBaseHandler): #ESTE ES EL HANDLER
    
    def handle(self, comando: CrearRegulacion): #ACA RECIBE EL COMANDO POR PARAMETRO

        regulacion_dto = RegulacionDTO(id=comando.id, nombre=comando.nombre, region=comando.region, payload= comando.payload, 
                                       fecha_actualizacion= comando.fecha_actualizacion)
        regulacion: Regulacion = self.fabrica_auditorias.crear_objeto(regulacion_dto, MapeadorRegulacion())
        regulacion.crear_regulacion(regulacion)
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioRegulaciones)
        repositorio_eventos = self.fabrica_repositorio.crear_objeto(RepositorioEventosRegulaciones)
        print("==========PASO#5============")
        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, regulacion, repositorio_eventos_func=repositorio_eventos.agregar)        
        print("==========PASO#44444444444444 COMMIT============")
        UnidadTrabajoPuerto.commit()


@comando.register(CrearRegulacion)
def ejecutar_comando_crear_regulacion(comando: CrearRegulacion):
    print("     ")
    print("==========PASO#1 SOLICITAR EJEUCTAR COMANDO============")
    handler = CrearRegulacionHandler()
    handler.handle(comando)
    