from pulsar import schema

from seedwork.infrastructure.schema.v1.commands import IntegrationCommand
from seedwork.infrastructure.schema.v1.header import CommandHeader


class StartDataIntakePayload(schema.Record):
    provider_id = schema.String()
    correlation_id = schema.String()


class CommandStartDataIntake(IntegrationCommand, schema.Record):
    data = StartDataIntakePayload()
    header = CommandHeader()
