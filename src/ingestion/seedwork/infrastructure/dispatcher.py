from abc import ABC
from functools import singledispatch

from seedwork.domain.events import DomainEvent
from seedwork.infrastructure.utils import broker_host
import pulsar


class Dispatcher(ABC):

    def publish_to_broker(
        self,
        message: pulsar.schema.Record,
        topic: str,
        schema: pulsar.schema.AvroSchema,
    ):
        client = pulsar.Client(broker_host())
        producer = client.create_producer(topic=topic, schema=schema)
        producer.send(message)
        client.close()


@singledispatch
def dispatch_event(event: DomainEvent):
    raise NotImplementedError(f"No dispatcher for event {type(event).__name__}")
