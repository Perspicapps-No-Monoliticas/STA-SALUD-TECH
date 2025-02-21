from abc import ABC, abstractmethod

from seedwork.infraestructure.utils import broker_host
from seedwork.application.commands import Command
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
