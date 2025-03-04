from pulsar import schema

from seedwork.infrastructure.schema.v1.events import IntegrationForCoreographyEvent
from seedwork.infrastructure.schema.v1.header import EventHeader


class DataCanonizationPayload(schema.Record):
    provider_id = schema.String()
    anonimization_id = schema.String()
    ingestion_id = schema.String()
    repository_in_path = schema.String()
    correlation_id = schema.String()
    canonization_id = schema.String()
    country_iso = schema.String()
    created_at = schema.String()
    updated_at = schema.String()


class AnonimizacionFinalizadaPayload(schema.Record):
    id_correlacion = schema.String()
    id_anonimizacion = schema.String()
    id_ingestion = schema.String()
    id_proveedor = schema.String()
    region = schema.String()
    ruta_repositorio = schema.String()


class EventDataCanonizationCreated(IntegrationForCoreographyEvent, schema.Record):
    data = DataCanonizationPayload()
    header = EventHeader()


class EventDataCanonizationStarted(IntegrationForCoreographyEvent, schema.Record):
    data = DataCanonizationPayload()
    header = EventHeader()


class EventDataCanonizationCompleted(IntegrationForCoreographyEvent, schema.Record):
    data = DataCanonizationPayload()
    header = EventHeader()


class EventoAnonimizacionFinalizada(schema.Record):
    data = AnonimizacionFinalizadaPayload()
    header = EventHeader()
