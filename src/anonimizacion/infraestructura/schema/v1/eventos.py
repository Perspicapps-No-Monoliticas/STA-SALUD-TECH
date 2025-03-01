from typing import Optional
from pulsar.schema import Record, String
from seedwork.infraestructura.schema.v1.eventos import EventoIntegracion, IntegrationForCoreographyEvent

class DataIngestionPayload(Record):
    data_ingestion_id: str
    provider_id: str
    status: str
    repository_out_path: Optional[str]
    created_at: str
    updated_at: str
    country_iso: str

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
