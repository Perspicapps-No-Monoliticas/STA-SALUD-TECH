from .messages import Message
from seedwork.infrastructure.varaibles import COUNTRY_CODE


class IntegrationEvent(Message):
    service_name: str = "integration"
    country_iso: str = COUNTRY_CODE


class IntegrationForCoreographyEvent(IntegrationEvent):
    correlation_id: str
    data: Message
