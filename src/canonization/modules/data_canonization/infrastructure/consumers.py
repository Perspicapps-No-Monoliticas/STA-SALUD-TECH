import logging
import uuid

from pulsar.schema import AvroSchema
import pulsar


import modules.data_canonization.infrastructure.command_dispatcher  # type: ignore
from modules.data_canonization.infrastructure.schema.v1.commands import (
    CommandStartDataCanonization,
)
from modules.data_canonization.infrastructure.schema.v1.events import (
    EventDataAnonimizationCompleted,
    AnonimizacionFinalizadaPayload,
)
from modules.data_canonization.application.commands.start_new_canonization import (
    StartDataCanonizationCommand,
)
from seedwork.infrastructure.consumer import (
    TopicConsumer,
    start_threads_for_all_consumers,
)
from seedwork.application.commands import execute_command, dispatch_command

from . import constants


class CreateDataCanonizationConsumer(TopicConsumer):
    TOPIC = constants.START_DATA_CANONIZATION_V1_TOPIC
    SUBSCRIPTION_NAME = "data-canonization-start-command"
    SCHEMA = AvroSchema(CommandStartDataCanonization)

    def process_message(self, message: pulsar.Message):
        payload: CommandStartDataCanonization = message.value()
        logging.info(f"Processing message {message.message_id()}")
        command = StartDataCanonizationCommand(
            provider_id=uuid.UUID(payload.data.provider_id),
            anonimization_id=uuid.UUID(payload.data.anonimization_id),
            ingestion_id=uuid.UUID(payload.data.ingestion_id),
            repository_in_path=payload.data.repository_in_path,
            correlation_id=uuid.UUID(payload.data.correlation_id),
        )
        execute_command(command)


class ListenToAnonimizationCompletedConsumer(TopicConsumer):
    TOPIC = constants.ANONIMIZATION_COMPLETED_V1_TOPIC
    SUBSCRIPTION_NAME = "anonimization-completed-event"
    SCHEMA = AvroSchema(EventDataAnonimizationCompleted)

    def process_message(self, message: pulsar.Message):
        payload: AnonimizacionFinalizadaPayload = message.value()
        logging.info(f"Processing message {message.message_id()}")
        command = StartDataCanonizationCommand(
            provider_id=uuid.UUID(payload.data.id_proveedor),
            anonimization_id=uuid.UUID(payload.data.id_anonimizacion),
            ingestion_id=uuid.UUID(payload.data.id_ingestion),
            repository_in_path=payload.data.ruta_repositorio,
            correlation_id=uuid.UUID(payload.data.id_correlacion),
        )

        dispatch_command(command)


def init_consumers():
    consumers = [
        CreateDataCanonizationConsumer(),
        ListenToAnonimizationCompletedConsumer(),
    ]
    start_threads_for_all_consumers(consumers)
