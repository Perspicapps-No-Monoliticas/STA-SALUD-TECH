from pulsar.schema import AvroSchema

from seedwork.application.commands import Command, dispatch_command
from seedwork.infraestructure.dispatcher import Dispatcher
from modules.data_source.application.commands import CreateDataSource
from modules.data_source.infraestrucuture.schema.v1.commands import (
    CommandCreateDataSource,
    CommandCreateDataSourcePayload,
    CredentialsPayload,
)
from . import constants


class DataSourceDispatcher(Dispatcher):

    def publish_create_data_source(self, command: CreateDataSource):
        payload = CommandCreateDataSourcePayload(
            name=command.name,
            description=command.description,
            type=command.type,
            credentials=CredentialsPayload(
                payload=command.credentials.payload, type=command.credentials.type
            ),
            provider_id=str(command.provider_id),
        )
        integration_command = CommandCreateDataSource(data=payload)
        self.publish_to_broker(
            message=integration_command,
            topic=constants.CREATE_DATA_SOURCE_V1_TOPIC,
            schema=AvroSchema(CommandCreateDataSource),
        )


@dispatch_command.register(CreateDataSource)
def dispatch_create_data_source(command: CreateDataSource):
    dispatcher = DataSourceDispatcher()
    dispatcher.publish_create_data_source(command)
