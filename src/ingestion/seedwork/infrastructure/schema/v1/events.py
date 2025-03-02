from pulsar import schema

from .messages import Message
from seedwork.infrastructure.varaibles import COUNTRY_CODE


class IntegrationEvent(Message):
    service_name = schema.String(default="integration")
    country_iso = schema.String(default=COUNTRY_CODE)


class IntegrationForCoreographyEvent(IntegrationEvent):
    correlation_id = schema.String()
    data = Message()
