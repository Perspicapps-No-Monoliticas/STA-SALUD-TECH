from pulsar import schema
from seedwork.infrastructure.schema.v1.commands import IntegrationCommand
from seedwork.infrastructure.schema.v1.header import CommandHeader


class CredentialsPayload(schema.Record):
    payload = schema.Map(schema.String())
    type = schema.String()


class CreateDataSourcePayload(schema.Record):
    name = schema.String()
    description = schema.String()
    type = schema.String()
    credentials = CredentialsPayload()
    provider_id = schema.String()


class CommandCreateDataSource(IntegrationCommand, schema.Record):
    data = CreateDataSourcePayload()
    header = CommandHeader()
