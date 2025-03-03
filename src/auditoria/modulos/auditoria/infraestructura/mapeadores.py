
from seedwork.dominio.repositorios import Mapeador
from seedwork.infraestructura.utils import unix_time_millis
from modulos.auditoria.dominio.entidades import  Regulacion
from modulos.auditoria.dominio.eventos import RegulacionCreada, EventoRegulacion

from .dto import Regulacion as RegulacionDTO
from .excepciones import NoExisteImplementacionParaTipoFabricaExcepcion
from pulsar.schema import *

class MapadeadorEventosRegulacion(Mapeador):

    # payloades aceptadas
    payloads = ('v1',)

    LATEST_payload = payloads[0]

    def __init__(self):
        self.router = {
            RegulacionCreada: self._entidad_a_regulacion_creada
        }

    def obtener_tipo(self) -> type:
        return EventoRegulacion.__class__

    def es_payload_valida(self, payload):
        for v in self.payloads:
            if v == payload:
                return True
        return False

    def _entidad_a_regulacion_creada(self, entidad: RegulacionCreada, payload=LATEST_payload):
        print(f"ENTRA A RegulacionCreadaPayloadd{entidad}")
        def v1(evento):
            from .schema.v1.eventos import RegulacionCreadaPayload, EventoRegulacionCreada            

            payload = RegulacionCreadaPayload(
                id_regulacion=str(evento.id_regulacion), 
                nombre=str(evento.nombre),           
                payload=str(evento.payload),           
                region=str(evento.region),                   
                fecha_creacion=int(unix_time_millis(evento.fecha_creacion))
            )
            evento_integracion = EventoRegulacionCreada(id=str(evento.id))
            evento_integracion.id = str(evento.id)
            evento_integracion.time = int(unix_time_millis(evento.fecha_creacion))
            evento_integracion.specpayload = str(payload)
            evento_integracion.type = 'RegulacionCreada'
            evento_integracion.datacontenttype = 'AVRO'
            evento_integracion.service_name = 'sta'
            evento_integracion.data = payload
            print("RETORNA RegulacionCreadaPayload")
            return evento_integracion
                    
        if not self.es_payload_valida(payload):
            raise Exception(f'No se sabe procesar la payload {payload}')

        if payload == 'v1':
            return v1(entidad)       

    def entidad_a_dto(self, entidad: EventoRegulacion, payload=LATEST_payload) -> RegulacionDTO:
        if not entidad:
            raise NoExisteImplementacionParaTipoFabricaExcepcion
        func = self.router.get(entidad.__class__, None)

        if not func:
            raise NoExisteImplementacionParaTipoFabricaExcepcion

        return func(entidad, payload=payload)

    def dto_a_entidad(self, dto: RegulacionDTO, payload=LATEST_payload) -> Regulacion:
        raise NotImplementedError


class MapeadorRegulacion(Mapeador):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return Regulacion.__class__

    def entidad_a_dto(self, entidad: Regulacion) -> RegulacionDTO:
        
        regulacion_dto = RegulacionDTO()
        regulacion_dto.id = str(entidad.id)
        regulacion_dto.nombre = str(entidad.nombre)
        regulacion_dto.region = str(entidad.region)
        regulacion_dto.payload = str(entidad.payload)
        regulacion_dto.fecha_creacion = entidad.fecha_creacion
        regulacion_dto.fecha_actualizacion = entidad.fecha_actualizacion        

        return regulacion_dto

    def dto_a_entidad(self, dto: RegulacionDTO) -> Regulacion:
        regulacion = Regulacion(dto.id, dto.fecha_creacion, dto.fecha_actualizacion)
        return regulacion