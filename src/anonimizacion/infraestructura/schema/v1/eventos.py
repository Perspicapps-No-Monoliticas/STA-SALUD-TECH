from pulsar.schema import Record, String, Map
from seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

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
