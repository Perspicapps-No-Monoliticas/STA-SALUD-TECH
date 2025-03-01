import logging
import uuid

from pulsar.schema import AvroSchema
import pulsar

from modules.data_canonization.infraestrucuture.schema.v1.commands import (
    CommandStartDataCanonization,
)
from modules.data_canonization.application.commands.start_new_canonization import (
    StartDataCanonizationCommand,
)
from seedwork.infraestructure.consumer import (
    TopicConsumer,
    start_threads_for_all_consumers,
)
from seedwork.application.commands import execute_command
from . import constants


class CreateDataCanonizationConsumer(TopicConsumer):
    TOPIC = constants.START_DATA_CANONIZATION_V1_TOPIC
    SUBSCRIPTION_NAME = "data-ingestion-start-command"
    SCHEMA = AvroSchema(CommandStartDataCanonization)

    def process_message(self, message: pulsar.Message):
        payload: CommandStartDataCanonization = message.value()
        logging.info(f"Processing message {message.message_id()}")
        command = StartDataCanonizationCommand(
            provider_id=uuid.UUID(payload.data.provider_id),
            anonimization_id=uuid.UUID(payload.data.anonimization_id),
            ingestion_id=uuid.UUID(payload.data.ingestion_id),
            repository_in_path=payload.data.repository_in_path,
        )
        execute_command(command)


def init_consumers():
    consumers = [CreateDataCanonizationConsumer()]
    start_threads_for_all_consumers(consumers)
