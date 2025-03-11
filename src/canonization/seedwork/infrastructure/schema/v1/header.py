import uuid

from pulsar import schema
from seedwork.infrastructure.utils import time_millis
from seedwork.infrastructure.varaibles import COUNTRY_CODE


class EventHeader(schema.Record):
    id = schema.String(default=str(uuid.uuid4()))
    ingestion = schema.Long(default=time_millis())
    specversion = schema.String("v1.0")
    type = schema.String("event")
    datacontenttype = schema.String("json")
    service_name = schema.String(default="canonization")
    country_iso = schema.String(default=COUNTRY_CODE)
    correlation_id = schema.String(default=str(uuid.uuid4()))


class CommandHeader(schema.Record):
    id = schema.String(default=str(uuid.uuid4()))
    ingestion = schema.Long(default=time_millis())
    specversion = schema.String("v1.0")
    type = schema.String("event")
    datacontenttype = schema.String("json")
    service_name = schema.String(default="canonization")
    country_iso = schema.String(default=COUNTRY_CODE)
    correlation_id = schema.String(default=str(uuid.uuid4()))
