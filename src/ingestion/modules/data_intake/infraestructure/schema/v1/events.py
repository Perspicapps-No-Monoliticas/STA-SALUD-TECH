from typing import Optional

from pulsar import schema

from seedwork.infraestructure.schema.v1.events import IntegrationForCoreographyEvent


class DataIngestionPayload(schema.Record):
    data_ingestion_id: str
    provider_id: str
    status: str
    repository_out_path: Optional[str]
    created_at: str
    updated_at: str
    country_iso: str


class DataIngestionCreated(IntegrationForCoreographyEvent):
    data = DataIngestionPayload()


class DataIngestionStarted(IntegrationForCoreographyEvent):
    data = DataIngestionPayload()


class DataIngestionFinished(IntegrationForCoreographyEvent):
    data = DataIngestionPayload()
