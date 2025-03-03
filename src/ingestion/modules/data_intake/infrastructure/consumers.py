import logging
import uuid

from pulsar.schema import AvroSchema
import pulsar

from modules.data_intake.infrastructure.schema.v1.commands import (
    CommandStartDataIntake,
)
from modules.data_intake.application.commands.start_new_ingestion import (
    StartDataIntakeCommand,
)
from seedwork.infrastructure.consumer import (
    TopicConsumer,
    start_threads_for_all_consumers,
)
from seedwork.application.commands import execute_command
from . import constants


class CreateDataIntakeConsumer(TopicConsumer):
    TOPIC = constants.START_DATA_INGESTION_V1_TOPIC
    SUBSCRIPTION_NAME = "data-ingestion-start-command"
    SCHEMA = AvroSchema(CommandStartDataIntake)

    def process_message(self, message: pulsar.Message):
        payload: CommandStartDataIntake = message.value()
        logging.info(f"Processing message {message.message_id()}")
        command = StartDataIntakeCommand(
            provider_id=uuid.UUID(payload.data.provider_id),
            correlation_id=uuid.UUID(payload.data.correlation_id),
        )
        execute_command(command)


def init_consumers():
    consumers = [CreateDataIntakeConsumer()]
    start_threads_for_all_consumers(consumers)
