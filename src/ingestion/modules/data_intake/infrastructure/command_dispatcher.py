from pulsar.schema import AvroSchema

from seedwork.application.commands import dispatch_command
from seedwork.infrastructure.dispatcher import Dispatcher
from modules.data_intake.application.commands import StartDataIntakeCommand
from modules.data_intake.infrastructure.schema.v1.commands import (
    CommandStartDataIntake,
)
from modules.data_intake.infrastructure.schema.v1.common import StartDataIntakePayload
from . import constants


class DataIntakeDispatcher(Dispatcher):

    def publish_start_data_intake(self, command: StartDataIntakeCommand):
        payload = StartDataIntakePayload(
            provider_id=str(command.provider_id),
            correlation_id=str(command.correlation_id),
        )
        integration_command = CommandStartDataIntake(data=payload)
        self.publish_to_broker(
            message=integration_command,
            topic=constants.START_DATA_INGESTION_V1_TOPIC,
            schema=AvroSchema(CommandStartDataIntake),
        )


@dispatch_command.register(StartDataIntakeCommand)
def dispatch_create_data_intake(command: StartDataIntakeCommand):
    dispatcher = DataIntakeDispatcher()
    dispatcher.publish_start_data_intake(command)
