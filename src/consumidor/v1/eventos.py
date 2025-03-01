from pulsar.schema import Record, String
from seedwork.infraestructura.schema.v1.eventos import EventoIntegracion

class AnonimizacionIniciadaPayload(Record):
    id_ingestion = String()
    id_proveedor = String()
    nombre_evento = String()

class AnonimizacionFinalizadaPayload(Record):
    id_ingestion = String()
    id_proveedor = String()
    nombre_evento = String()

class EventoAnonimizacionIniciada(EventoIntegracion):
    data = AnonimizacionIniciadaPayload()

class EventoAnonimizacionFinalizada(EventoIntegracion):
    data = AnonimizacionFinalizadaPayload()