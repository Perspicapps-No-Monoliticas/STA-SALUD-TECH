from pulsar.schema import *
from seedwork.infraestructura.schema.v1.eventos import EventoIntegracion
from seedwork.infraestructura.utils import time_millis
import uuid

class Requisito(Record):
    codigo = String()
    descripcion = String()
    obligatorio = Boolean()

class RegulacionCreadaPayload(Record):
    id_regulacion = String()
    nombre = String()
    region = String()
    payload = String()
    requisitos = Array(Requisito())
    fecha_creacion = Long()       

class EventoRegulacionCreada(EventoIntegracion):
    # NOTE La librería Record de Pulsar no es capaz de reconocer campos heredados, 
    # por lo que los mensajes al ser codificados pierden sus valores
    # Dupliqué el los cambios que ya se encuentran en la clase Mensaje
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specpayload = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = RegulacionCreadaPayload()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
class CredentialsPayload(Record):
    payload = Map(String())
    type = String()

class CreateDataSourcePayload(Record):
    name = String()
    description = String()
    type = String()
    credentials = CredentialsPayload()
    provider_id = String()

class EventDataSourceCreatedPayload(CreateDataSourcePayload):
    id = String()
    created_at = String()
    updated_at = String()

class AnonimizacionIniciadaPayload(Record):
    id_ingestion = String()
    id_proveedor = String()
    nombre_evento = String()

class AnonimizacionFinalizadaPayload(Record):
    id_ingestion = String()
    id_proveedor = String()
    nombre_evento = String()

class EventoAnonimizacionIniciada(EventoIntegracion):
    data = AnonimizacionIniciadaPayload()

class EventoAnonimizacionFinalizada(EventoIntegracion):
    data = AnonimizacionFinalizadaPayload()

class EventDataSourceCreated(EventoIntegracion):
    data = EventDataSourceCreatedPayload()