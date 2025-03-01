from infraestructura.schema import Mensaje

class EventoIntegracion(Mensaje):
    ...

class IntegrationEvent(Mensaje):
    service_name: str = "integration"
    country_iso: str = ""

class IntegrationForCoreographyEvent(IntegrationEvent):
    correlation_id: str
    data: Mensaje