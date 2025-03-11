from pulsar import schema


class EventHeader(schema.Record):
    id = schema.String()
    ingestion = schema.Long()
    specversion = schema.String()
    type = schema.String()
    datacontenttype = schema.String()
    service_name = schema.String()
    country_iso = schema.String()
    correlation_id = schema.String()

class CommandHeader(schema.Record):
    id = schema.String()
    ingestion = schema.Long()
    specversion = schema.String()
    type = schema.String()
    datacontenttype = schema.String()
    service_name = schema.String()
    country_iso = schema.String()
    correlation_id = schema.String()
class StartDataIntakePayload(schema.Record):
    provider_id = schema.String()
    correlation_id = schema.String()


class CommandStartDataIntake(schema.Record):
    data = StartDataIntakePayload()
    header = CommandHeader()


class DataIngestionPayload(schema.Record):
    data_ingestion_id = schema.String()
    provider_id = schema.String()
    status = schema.String()
    repository_out_path = schema.String()
    created_at = schema.String()
    updated_at = schema.String()
    country_iso = schema.String()


class DataIngestionCreated(schema.Record):
    data = DataIngestionPayload()
    header = EventHeader()


class DataIngestionStarted(schema.Record):
    data = DataIngestionPayload()
    header = EventHeader()


class DataIngestionFinished(schema.Record):
    data = DataIngestionPayload()
    header = EventHeader()


class AnonimizacionFinalizadaPayload(schema.Record):
    id_correlacion = schema.String()
    id_anonimizacion = schema.String()
    id_ingestion = schema.String()
    id_proveedor = schema.String()
    region = schema.String()
    ruta_repositorio = schema.String()


class EventoAnonimizacionFinalizada(schema.Record):
    data = AnonimizacionFinalizadaPayload()
    header = EventHeader()


class StartDataCanonizationPayload(schema.Record):
    provider_id = schema.String()
    anonimization_id = schema.String()
    ingestion_id = schema.String()
    repository_in_path = schema.String()
    correlation_id = schema.String()


class CommandStartDataCanonization(schema.Record):
    data = StartDataCanonizationPayload()
    header = CommandHeader()


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


class EventDataCanonizationCreated(schema.Record):
    data = DataCanonizationPayload()
    header = EventHeader()


class EventDataCanonizationStarted(schema.Record):
    data = DataCanonizationPayload()
    header = EventHeader()


class EventDataCanonizationCompleted(schema.Record):
    data = DataCanonizationPayload()
    header = EventHeader()
