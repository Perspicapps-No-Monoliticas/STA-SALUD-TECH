from seedwork.infraestructure.schema.v1.commands import IntegrationCommand
from .common import CreateDataSourcePayload


class CommandCreateDataSource(IntegrationCommand):
    data = CreateDataSourcePayload()
    specversion = "1.0"
