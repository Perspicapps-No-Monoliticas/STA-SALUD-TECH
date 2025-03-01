from seedwork.infrastructure.schema.v1.commands import IntegrationCommand
from .common import StartDataIntakePayload


class CommandStartDataIntake(IntegrationCommand):
    data = StartDataIntakePayload()
    specversion = "1.0"
