from threading import Thread
import logging
import traceback
from abc import ABC, abstractmethod
from typing import List

import pulsar

from config import BROKER_URL
from models import SessionLocal, SagaLog


class TopicConsumer(Thread, ABC):

    TOPIC: str
    SUBSCRIPTION_NAME: str
    SCHEMA: pulsar.schema.AvroSchema

    def process_message(self, message: pulsar.Message):
        payload = message.value()
        session = SessionLocal()
        try:
            saga_log = SagaLog(
                correlation_id=payload.header.correlation_id,
                component=payload.header.service_name,
                action_name= self.SCHEMA.__class__.__name__,
                type=payload.header.type,
                entity_id=self.get_entity_id(payload),
                event_at=payload.header.ingestion,
            )
            session.add(saga_log)
            session.commit()
        except Exception:
            session.rollback()
            logging.error(f"Error saving message {message}")
            traceback.print_exc()
        finally:
            session.close()

    def get_entity_id(self, payload):
        return None

    def run(self):
        client = None
        try:
            client = pulsar.Client(BROKER_URL)
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
        consumer().start()
