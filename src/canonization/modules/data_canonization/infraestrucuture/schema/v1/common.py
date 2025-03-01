from pulsar import schema


class StartDataCanonizationPayload(schema.Record):
    provider_id = schema.String()
    anonimization_id = schema.String()
    ingestion_id = schema.String()
    repository_in_path = schema.String()
