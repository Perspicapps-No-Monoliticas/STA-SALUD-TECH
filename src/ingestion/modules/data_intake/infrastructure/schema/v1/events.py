from pulsar import schema

from seedwork.infrastructure.schema.v1.events import IntegrationForCoreographyEvent
from seedwork.infrastructure.schema.v1.header import EventHeader


class DataIngestionPayload(schema.Record):
    data_ingestion_id = schema.String()
    provider_id = schema.String()
    status = schema.String()
    repository_out_path = schema.String()
    created_at = schema.String()
    updated_at = schema.String()
    country_iso = schema.String()


class DataIngestionCreated(IntegrationForCoreographyEvent, schema.Record):
    data = DataIngestionPayload()
    header = EventHeader()


class DataIngestionStarted(IntegrationForCoreographyEvent, schema.Record):
    data = DataIngestionPayload()
    header = EventHeader()


class DataIngestionFinished(IntegrationForCoreographyEvent, schema.Record):
    data = DataIngestionPayload()
    header = EventHeader()
