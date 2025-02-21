from pulsar import schema

from seedwork.infraestructure.schema.v1.commands import IntegrationCommand


class CredentialsPayload(schema.Record):
    payload = schema.Map(schema.String())
    source = schema.String


class CommandCreateDataSourcePayload(schema.Record):
    name = schema.String()
    description = schema.String()
    type = schema.String()
    credentials = CredentialsPayload()
    provider_id = schema.Integer()


class CommandCreateDataSource(IntegrationCommand):
    data = CommandCreateDataSourcePayload()
