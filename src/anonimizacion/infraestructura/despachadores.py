import pulsar
from pulsar.schema import AvroSchema
from aplicacion.dto import InformacionMedicaDTO
from dominio.entidades import InformacionMedica
from infraestructura import utils
from infraestructura.schema.v1.eventos import AnonimizacionFinalizadaPayload, AnonimizacionIniciadaPayload, EventoAnonimizacionFinalizada, EventoAnonimizacionIniciada
from dominio.eventos import TokenizadoIniciado, TokenizadoRealizado,AnonimizadoPorModeloRealizado
from seedwork.dominio.eventos import EventoDominio
from seedwork.infraestructura.schema.v1.header import EventHeader

class Despachador:
    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f"pulsar://{utils.broker_host()}:6650")
        publicador = cliente.create_producer(topico, schema=schema)
        publicador.send(mensaje)
        cliente.close()

    def publicar_evento(self, evento: EventoDominio, topico):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del evento
        if isinstance(evento,TokenizadoIniciado):
            pass
        elif isinstance(evento,AnonimizadoPorModeloRealizado): 
            payload = AnonimizacionFinalizadaPayload(
                id_correlacion = str(evento.data.correlation_id),
                id_anonimizacion=str(evento.data.token),
                id_ingestion=str(evento.data.data_ingestion_id), 
                id_proveedor=str(evento.data.provider_id),
                region=str(evento.data.country_iso),
                ruta_repositorio=str(evento.data.repository_out_path)
            )
            header = EventHeader(correlation_id=str(evento.data.correlation_id))
            evento_integracion = EventoAnonimizacionFinalizada(data=payload, header=header)
            self._publicar_mensaje(evento_integracion, topico, AvroSchema(evento_integracion.__class__))
        else:
            print(f"Evento no soportado: {evento}")
