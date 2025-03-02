from pulsar import schema

from seedwork.infrastructure.schema.v1.events import IntegrationForCoreographyEvent
from seedwork.infrastructure.schema.v1.messages import Message
from .common import StartDataCanonizationPayload


class DataCanonizationPayload(StartDataCanonizationPayload):
    canonization_id = schema.String()
    country_iso = schema.String()
    created_at = schema.String()
    updated_at = schema.String()


class EventDataCanonizationCreated(IntegrationForCoreographyEvent):
    data = DataCanonizationPayload()


class EventDataCanonizationStarted(IntegrationForCoreographyEvent):
    data = DataCanonizationPayload()


class EventDataCanonizationCompleted(IntegrationForCoreographyEvent):
    data = DataCanonizationPayload()


class AnonimizacionFinalizadaPayload(schema.Record):
    id_correlacion = schema.String()
    id_anonimizacion = schema.String()
    id_ingestion = schema.String()
    id_proveedor = schema.String()
    region = schema.String()
    ruta_repositorio = schema.String()


class EventoAnonimizacionFinalizada(Message):
    data = AnonimizacionFinalizadaPayload()
