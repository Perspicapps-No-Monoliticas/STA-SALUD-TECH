from pulsar.schema import AvroSchema

from seedwork.application.commands import dispatch_command
from seedwork.infraestructure.dispatcher import Dispatcher
from modules.data_canonization.application.commands import StartDataCanonizationCommand
from modules.data_canonization.infraestrucuture.schema.v1.commands import (
    CommandStartDataCanonization,
)
from modules.data_canonization.infraestrucuture.schema.v1.common import (
    StartDataCanonizationPayload,
)
from . import constants


class DataCanonizationDispatcher(Dispatcher):

    def publish_start_data_canonization(self, command: StartDataCanonizationCommand):
        payload = StartDataCanonizationPayload(
            provider_id=str(command.provider_id),
            anonimization_id=str(command.anonimization_id),
            ingestion_id=str(command.ingestion_id),
            repository_in_path=command.repository_in_path,
        )
        integration_command = CommandStartDataCanonization(data=payload)
        self.publish_to_broker(
            message=integration_command,
            topic=constants.START_DATA_CANONIZATION_V1_TOPIC,
            schema=AvroSchema(CommandStartDataCanonization),
        )


@dispatch_command.register(StartDataCanonizationCommand)
def dispatch_create_data_canonization(command: StartDataCanonizationCommand):
    dispatcher = DataCanonizationDispatcher()
    dispatcher.publish_start_data_canonization(command)
