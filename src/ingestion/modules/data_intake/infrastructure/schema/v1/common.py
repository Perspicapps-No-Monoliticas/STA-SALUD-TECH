from pulsar import schema


class StartDataIntakePayload(schema.Record):
    provider_id = schema.String()
    correlation_id = schema.String()
