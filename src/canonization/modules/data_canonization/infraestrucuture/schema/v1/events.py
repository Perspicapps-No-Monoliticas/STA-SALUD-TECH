from pulsar import schema

from seedwork.infraestructure.schema.v1.events import IntegrationEvent
from .common import StartDataCanonizationPayload


class EventDataCanonizationCreatedPayload(StartDataCanonizationPayload):
    id = schema.String()
    created_at = schema.String()
    updated_at = schema.String()


class EventDataCanonizationCreated(IntegrationEvent):
    data = EventDataCanonizationCreatedPayload()
