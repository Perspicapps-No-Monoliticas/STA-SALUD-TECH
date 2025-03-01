import pulsar
from pulsar.schema import AvroSchema
from infraestructura import utils


class Despachador:
    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f"pulsar://{utils.broker_host()}:6650")
        publicador = cliente.create_producer(topico, schema=schema)
        publicador.send(mensaje)
        cliente.close()

    def publicar_evento(self, evento_integracion, topico):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del evento
        self._publicar_mensaje(evento_integracion, topico, AvroSchema(evento_integracion.__class__))

    #def publicar_comando(self, comando, topico):
    #    # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del comando
    #    payload = ComandoCrearReservaPayload(
    #        id_usuario=str(comando.id_usuario)
    #        # agregar itinerarios
    #    )
    #    comando_integracion = ComandoCrearReserva(data=payload)
    #    self._publicar_mensaje(comando_integracion, topico, AvroSchema(ComandoCrearReserva))
