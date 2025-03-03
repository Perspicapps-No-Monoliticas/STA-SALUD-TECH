from pulsar import schema

from seedwork.infrastructure.schema.v1.commands import IntegrationCommand
from seedwork.infrastructure.schema.v1.header import CommandHeader


class StartDataCanonizationPayload(schema.Record):
    provider_id = schema.String()
    anonimization_id = schema.String()
    ingestion_id = schema.String()
    repository_in_path = schema.String()
    correlation_id = schema.String()


class CommandStartDataCanonization(IntegrationCommand, schema.Record):
    data = StartDataCanonizationPayload()
    header = CommandHeader()
