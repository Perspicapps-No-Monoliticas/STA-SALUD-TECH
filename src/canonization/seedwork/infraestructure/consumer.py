from threading import Thread
import logging
import traceback
from abc import ABC, abstractmethod
from typing import List

import pulsar

from seedwork.infraestructure.utils import broker_host


class TopicConsumer(Thread, ABC):

    TOPIC: str
    SUBSCRIPTION_NAME: str
    SCHEMA: pulsar.schema.AvroSchema

    @abstractmethod
    def process_message(self, message: pulsar.Message):
        raise NotImplementedError()

    def run(self):
        client = None
        try:
            client = pulsar.Client(broker_host())
            consumer = client.subscribe(
                topic=self.TOPIC,
                subscription_name=self.SUBSCRIPTION_NAME,
                schema=self.SCHEMA,
            )
            while True:
                msg = consumer.receive()
                try:
                    print(f"Received message: {msg.value()}")
                    consumer.acknowledge(msg)
                    self.process_message(msg)
                except Exception:
                    consumer.negative_acknowledge(msg)
                    logging.error(f"Error consuming message {msg}")
                    traceback.print_exc()

        except Exception:
            logging.error(f"Error starting consumer  {self.TOPIC}")
            traceback.print_exc()
            if client:
                client.close()


def start_threads_for_all_consumers(consumers: List[TopicConsumer]):
    for consumer in consumers:
        consumer.start()
