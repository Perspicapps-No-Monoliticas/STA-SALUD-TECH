from pulsar import schema


class CredentialsPayload(schema.Record):
    payload = schema.Map(schema.String())
    type = schema.String()


class CreateDataSourcePayload(schema.Record):
    name = schema.String()
    description = schema.String()
    type = schema.String()
    credentials = CredentialsPayload()
    provider_id = schema.String()
