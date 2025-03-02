from pulsar.schema import Record, String
from seedwork.infraestructura.schema.v1.eventos import EventoIntegracion, IntegrationForCoreographyEvent

class DataIngestionPayload(Record):
    data_ingestion_id = String()
    provider_id = String()
    status = String()
    repository_out_path = String()
    created_at = String()
    updated_at = String()
    country_iso = String()

class AnonimizacionIniciadaPayload(Record):
    id_ingestion = String()
    id_proveedor = String()
    nombre_evento = String()

class AnonimizacionFinalizadaPayload(Record):
    id_correlacion = String()
    id_anonimizacion = String()
    id_ingestion = String()
    id_proveedor = String()
    region = String()
    ruta_repositorio = String()

class EventoAnonimizacionIniciada(EventoIntegracion):
    data = AnonimizacionIniciadaPayload()

class EventoAnonimizacionFinalizada(EventoIntegracion):
    data = AnonimizacionFinalizadaPayload()

class DataIngestionFinished(IntegrationForCoreographyEvent):
    data = DataIngestionPayload()
