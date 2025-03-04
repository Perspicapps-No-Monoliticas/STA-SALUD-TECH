import logging
import uuid

from pulsar.schema import AvroSchema
import pulsar

from modules.data_source.application.dto import CredentialsDTO
from modules.data_source.infrastructure.schema.v1.commands import (
    CommandCreateDataSource,
)
from modules.data_source.application.commands.create_data_source import CreateDataSource
from seedwork.infrastructure.consumer import (
    TopicConsumer,
    start_threads_for_all_consumers,
)
from seedwork.application.commands import execute_command
from . import constants


class CreateDataSourceCommandConsumer(TopicConsumer):
    TOPIC = constants.CREATE_DATA_SOURCE_V1_TOPIC
    SUBSCRIPTION_NAME = "data-source-creation-command"
    SCHEMA = AvroSchema(CommandCreateDataSource)

    def process_message(self, message: pulsar.Message):
        payload: CommandCreateDataSource = message.value()
        logging.info(f"Processing message {message.message_id()}")
        command = CreateDataSource(
            name=payload.data.name,
            description=payload.data.description,
            type=payload.data.type,
            credentials=CredentialsDTO(
                payload=payload.data.credentials.payload,
                type=payload.data.credentials.type,
            ),
            provider_id=uuid.UUID(payload.data.provider_id),
        )
        execute_command(command)


def init_consumers():
    consumers = [CreateDataSourceCommandConsumer()]
    start_threads_for_all_consumers(consumers)
