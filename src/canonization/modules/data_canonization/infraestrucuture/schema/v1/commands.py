from seedwork.infraestructure.schema.v1.commands import IntegrationCommand
from .common import StartDataCanonizationPayload


class CommandStartDataCanonization(IntegrationCommand):
    data = StartDataCanonizationPayload()
    specversion = "1.0"
