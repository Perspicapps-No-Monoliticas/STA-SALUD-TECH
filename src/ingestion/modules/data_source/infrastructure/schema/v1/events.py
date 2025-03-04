from pulsar import schema

from seedwork.infrastructure.schema.v1.events import IntegrationForCoreographyEvent
from seedwork.infrastructure.schema.v1.header import EventHeader


class CredentialsPayload(schema.Record):
    payload = schema.Map(schema.String())
    type = schema.String()


class EventDataSourceCreatedPayload(schema.Record):
    id = schema.String()
    created_at = schema.String()
    updated_at = schema.String()
    name = schema.String()
    description = schema.String()
    type = schema.String()
    credentials = CredentialsPayload()
    provider_id = schema.String()


class EventDataSourceCreated(IntegrationForCoreographyEvent, schema.Record):
    data = EventDataSourceCreatedPayload()
    header = EventHeader()
