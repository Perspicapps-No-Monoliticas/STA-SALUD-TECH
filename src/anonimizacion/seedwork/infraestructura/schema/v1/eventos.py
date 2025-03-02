from pulsar.schema import String

from seedwork.infraestructura.schema.v1.mensajes import Mensaje

class EventoIntegracion(Mensaje):
    ...

class IntegrationEvent(Mensaje):
    service_name = String(default="anonimization")
    country_iso = String()

class IntegrationForCoreographyEvent(IntegrationEvent):
    correlation_id=  String()
    data = Mensaje()