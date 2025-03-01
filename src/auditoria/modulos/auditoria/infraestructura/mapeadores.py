
from seedwork.dominio.repositorios import Mapeador
from seedwork.infraestructura.utils import unix_time_millis
from modulos.auditoria.dominio.objetos_valor import  Requisito
from modulos.auditoria.dominio.entidades import  Regulacion
from modulos.auditoria.dominio.eventos import RegulacionCreada, EventoRegulacion

from .dto import Regulacion as RegulacionDTO
from .dto import Requisito as RequisitoDTO
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
            requisitos = [{"codigo": req.codigo, "descripcion": req.descripcion, "obligatorio": req.obligatorio} for req in evento.requisitos] if evento.requisitos else []

            payload = RegulacionCreadaPayload(
                id_regulacion=str(evento.id_regulacion), 
                nombre=str(evento.nombre),           
                payload=str(evento.payload),           
                region=str(evento.region),        
                requisitos=requisitos,              
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

    def _procesar_requisito_dto(self, requisitos_dto: list) -> list[Requisito]:
        reqs = list()
        for req in requisitos_dto:
            requisito = Requisito()
            requisito.codigo=req.codigo
            requisito.descripcion=req.descripcion
            requisito.obligatorio=req.obligatorio
            reqs.append(requisito)

        return reqs

    def _procesar_requisito(self, requisito: any) -> list[RequisitoDTO]:
        requisitos_dto = list()

        requisito_dto = RequisitoDTO()
        requisito_dto.codigo = requisito.codigo
        requisito_dto.descripcion = requisito.descripcion
        requisito_dto.obligatorio = requisito.obligatorio

        requisitos_dto.append(requisito_dto)
        return requisitos_dto

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

        requisitos_dto = list()
        
        for requisito in entidad.requisitos:
            requisitos_dto.extend(self._procesar_requisito(requisito))

        regulacion_dto.requisitos = requisitos_dto

        return regulacion_dto

    def dto_a_entidad(self, dto: RegulacionDTO) -> Regulacion:
        regulacion = Regulacion(dto.id, dto.fecha_creacion, dto.fecha_actualizacion)
        regulacion.requisitos = list()

        requisitos_dto: list[RequisitoDTO] = dto.requisitos
        regulacion.requisitos.extend(self._procesar_requisito_dto(requisitos_dto))
        
        return regulacion