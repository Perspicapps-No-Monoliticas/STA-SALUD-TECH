from seedwork.infraestructura.proyecciones import Proyeccion, ProyeccionHandler
from seedwork.infraestructura.proyecciones import ejecutar_proyeccion as proyeccion
from modulos.auditoria.infraestructura.fabricas import FabricaRepositorio
from modulos.auditoria.infraestructura.repositorios import RepositorioRegulaciones
from modulos.auditoria.dominio.entidades import Regulacion
from modulos.auditoria.infraestructura.dto import Regulacion as RegulacionDTO

from seedwork.infraestructura.utils import millis_a_datetime
import datetime
import logging
import traceback
from abc import ABC, abstractmethod

class ProyeccionAuditoria(Proyeccion, ABC):
    @abstractmethod
    def ejecutar(self):
        ...

class ProyeccionAuditoriaLista(ProyeccionAuditoria):
    print("ENTRA PROYECCION REGULACIONES")
    def __init__(self, nombre_evento, payload):        
        self.nombre_evento = nombre_evento
        self.payload = payload     
    
    def ejecutar(self, db=None):
        if not db:
            logging.error('ERROR: DB del app no puede ser nula')
            return
        
        fabrica_repositorio = FabricaRepositorio()
        repositorio = fabrica_repositorio.crear_objeto(RepositorioRegulaciones)
        print(f"Agregar.. {self.nombre_evento}")
        print(f"Payload.. {self.payload}")
        repositorio.agregar(
            Regulacion(
                nombre=str(self.nombre_evento),
                payload=str(self.payload)))
        db.session.commit()

class ProyeccionAuditoriaHandler(ProyeccionHandler):
    
    def handle(self, proyeccion: ProyeccionAuditoria):

        # TODO El evento de creación no viene con todos los datos de itinerarios, esto tal vez pueda ser una extensión
        # Asi mismo estamos dejando la funcionalidad de persistencia en el mismo método de recepción. Piense que componente
        # podriamos diseñar para alojar esta funcionalidad
        from config.db import db

        proyeccion.ejecutar(db=db)
        

@proyeccion.register(ProyeccionAuditoriaLista)
def ejecutar_proyeccion_regulacion(proyeccion, app=None):
    print("REGISTRAR PROYECCION REGULACIONES")
    if not app:
        logging.error('ERROR: Contexto del app no puede ser nulo')
        return
    try:
        with app.app_context():
            handler = ProyeccionAuditoriaHandler()
            handler.handle(proyeccion)
            
    except:
        traceback.print_exc()
        logging.error('ERROR: Persistiendo!')
    