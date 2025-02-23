from pulsar import schema

from seedwork.infraestructure.schema.v1.events import IntegrationEvent
from .common import CreateDataSourcePayload


class EventDataSourceCreatedPayload(CreateDataSourcePayload):
    id = schema.String()
    created_at = schema.String()
    updated_at = schema.String()


class EventDataSourceCreated(IntegrationEvent):
    data = EventDataSourceCreatedPayload()
