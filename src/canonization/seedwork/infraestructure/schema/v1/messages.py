import uuid

from pulsar import schema
from seedwork.infraestructure.utils import time_millis


class Message(schema.Record):
    id = schema.String(default=str(uuid.uuid4()))
    time = schema.Long()
    ingestion = schema.Long(default=time_millis())
    specversion = schema.String()
    type = schema.String()
    datacontenttype = schema.String()
    service_name = schema.String()
