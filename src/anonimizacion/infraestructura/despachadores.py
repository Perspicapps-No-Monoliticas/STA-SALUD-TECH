import pulsar
from pulsar.schema import AvroSchema
from aplicacion.dto import InformacionMedicaDTO
from dominio.entidades import InformacionMedica
from infraestructura import utils
from infraestructura.schema.v1.eventos import AnonimizacionFinalizadaPayload, AnonimizacionIniciadaPayload, EventoAnonimizacionFinalizada, EventoAnonimizacionIniciada


class Despachador:
    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f"pulsar://{utils.broker_host()}:6650")
        publicador = cliente.create_producer(topico, schema=schema)
        publicador.send(mensaje)
        cliente.close()

    def publicar_evento(self, evento: InformacionMedicaDTO, topico):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del evento
        payload = AnonimizacionFinalizadaPayload(
            id_correlacion = str(evento.data.correlation_id),
            id_anonimizacion=str(evento.data.token),
            id_ingestion=str(evento.data.data_ingestion_id), 
            id_proveedor=str(evento.data.provider_id),
            region=str(evento.data.country_iso),
            ruta_repositorio=str(evento.data.repository_out_path)
        )
        evento_integracion = EventoAnonimizacionFinalizada(data=payload)
        self._publicar_mensaje(evento_integracion, topico, AvroSchema(evento_integracion.__class__))

