from pulsar.schema import AvroSchema

from seedwork.application.commands import dispatch_command
from seedwork.infrastructure.dispatcher import Dispatcher
from modules.data_source.application.commands import CreateDataSource
from modules.data_source.infrastructure.schema.v1.commands import (
    CommandCreateDataSource,
)
from modules.data_source.infrastructure.schema.v1.commands import (
    CredentialsPayload,
    CreateDataSourcePayload,
)
from . import constants


class DataSourceDispatcher(Dispatcher):

    def publish_create_data_source(self, command: CreateDataSource):
        payload = CreateDataSourcePayload(
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
