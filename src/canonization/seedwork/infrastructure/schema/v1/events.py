from pulsar import schema

from .messages import Message
from seedwork.infrastructure.varaibles import COUNTRY_CODE


class IntegrationEvent(Message):
    service_name: str = schema.String("integration")
    country_iso: str = schema.String(COUNTRY_CODE)


class IntegrationForCoreographyEvent(IntegrationEvent):
    correlation_id = schema.String()
    data = Message()
