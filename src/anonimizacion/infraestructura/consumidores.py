import pulsar, _pulsar
from pulsar.schema import *
import logging
import traceback

from aplicacion.comandos.realizar_anonimizado import AnonimizarInformacionMedica
from aplicacion.dto import InformacionMedicaDTO
from infraestructura.schema.v1.eventos import DataIngestionFinished
from infraestructura import utils
from seedwork.aplicacion.comandos import ejecutar_commando


def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f"pulsar://{utils.broker_host()}:6650")
        consumidor = cliente.subscribe(
            f"{utils.country_code()}-data-ingestion-finished-v1",
            consumer_type=_pulsar.ConsumerType.Shared,
            subscription_name="anonimization-component",
            schema=AvroSchema(DataIngestionFinished),
        )

        while True:
            mensaje = consumidor.receive()
            print(f"Evento recibido: {mensaje.value().data}")
            payload: DataIngestionFinished = mensaje.value()
            print(f"Payload: {payload.__dict__}")

            data = InformacionMedicaDTO(
                correlation_id=payload.correlation_id,
                data_ingestion_id=payload.data.data_ingestion_id,
                status=payload.data.status,
                provider_id=payload.data.provider_id,
                repository_out_path=payload.data.repository_out_path,
                created_at=payload.data.created_at,
                updated_at=payload.data.updated_at,
                country_iso=payload.data.country_iso,
            )

            # Process the anonymization
            comando = AnonimizarInformacionMedica(data)
            ejecutar_commando(comando)
            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error("ERROR: Suscribiendose al tópico de eventos!")
        traceback.print_exc()
        if cliente:
            cliente.close()
