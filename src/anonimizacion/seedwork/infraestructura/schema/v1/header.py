import uuid

from pulsar import schema
from seedwork.infraestructura.utils import time_millis, country_code


class EventHeader(schema.Record):
    id = schema.String(default=str(uuid.uuid4()))
    ingestion = schema.Long(default=time_millis())
    specversion = schema.String("v1.0")
    type = schema.String("event")
    datacontenttype = schema.String("json")
    service_name = schema.String(default="anonimization")
    country_iso = schema.String(default=country_code())
    correlation_id = schema.String(default=str(uuid.uuid4()))


class CommandHeader(schema.Record):
    id = schema.String(default=str(uuid.uuid4()))
    ingestion = schema.Long(default=time_millis())
    specversion = schema.String("v1.0")
    type = schema.String("event")
    datacontenttype = schema.String("json")
    service_name = schema.String(default="anonimization")
    country_iso = schema.String(default=country_code())
    correlation_id = schema.String(default=str(uuid.uuid4()))
