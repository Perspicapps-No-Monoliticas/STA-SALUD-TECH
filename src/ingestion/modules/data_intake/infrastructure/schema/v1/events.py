from typing import Optional

from pulsar import schema

from seedwork.infrastructure.schema.v1.events import IntegrationForCoreographyEvent


class DataIngestionPayload(schema.Record):
    data_ingestion_id = schema.String()
    provider_id = schema.String()
    status = schema.String()
    repository_out_path = schema.String()
    created_at = schema.String()
    updated_at = schema.String()
    country_iso = schema.String()


class DataIngestionCreated(IntegrationForCoreographyEvent):
    data = DataIngestionPayload()


class DataIngestionStarted(IntegrationForCoreographyEvent):
    data = DataIngestionPayload()


class DataIngestionFinished(IntegrationForCoreographyEvent):
    data = DataIngestionPayload()
