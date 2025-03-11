from pulsar.schema import AvroSchema

import topics
import schemas
from base_consumer import TopicConsumer


class CreateDataIngestionConsumer(TopicConsumer):
    TOPIC = topics.START_DATA_INGESTION_V1_TOPIC
    SUBSCRIPTION_NAME = "data-ingestion-start-command-log"
    SCHEMA = AvroSchema(schemas.CommandStartDataIntake)


class DatataingestionMixin:

    def get_entity_id(self, payload):
        return payload.data.data_ingestion_id


class DataIngestionCreatedConsumer(TopicConsumer, DatataingestionMixin):
    TOPIC = topics.DATA_INGESTION_CREATED_V1_TOPIC
    SUBSCRIPTION_NAME = "data-ingestion-created-log"
    SCHEMA = AvroSchema(schemas.DataIngestionCreated)


class DataIngestionStartedConsumer(TopicConsumer, DatataingestionMixin):
    TOPIC = topics.DATA_INGESTION_STARTED_V1_TOPIC
    SUBSCRIPTION_NAME = "data-ingestion-started-log"
    SCHEMA = AvroSchema(schemas.DataIngestionStarted)


class DataIngestionFinishedConsumer(TopicConsumer, DatataingestionMixin):
    TOPIC = topics.DATA_INGESTION_FINISHED_V1_TOPIC
    SUBSCRIPTION_NAME = "data-ingestion-finished-log"
    SCHEMA = AvroSchema(schemas.DataIngestionFinished)


class AnonimizationCompletedConsumer(TopicConsumer):
    TOPIC = topics.EVENTO_INTEGRACION_ANONIMIZACION_FINALIZADO
    SUBSCRIPTION_NAME = "anonimization-completed-log"
    SCHEMA = AvroSchema(schemas.EventoAnonimizacionFinalizada)

    def get_entity_id(self, payload):
        return payload.data.id_anonimizacion


class CreateDataCanonizationConsumer(TopicConsumer):
    TOPIC = topics.START_DATA_CANONIZATION_V1_TOPIC
    SUBSCRIPTION_NAME = "data-canonization-start-command-log"
    SCHEMA = AvroSchema(schemas.CommandStartDataCanonization)


class DataCanonizationMixin:

    def get_entity_id(self, payload):
        return payload.data.canonization_id


class DataCanonizationCreatedConsumer(TopicConsumer, DataCanonizationMixin):
    TOPIC = topics.DATA_CANONIZATION_CREATED_V1_TOPIC
    SUBSCRIPTION_NAME = "data-canonization-created-log"
    SCHEMA = AvroSchema(schemas.EventDataCanonizationCreated)


class DataCanonizationStartedConsumer(TopicConsumer, DataCanonizationMixin):
    TOPIC = topics.DATA_CANONIZATION_STARTED_V1_TOPIC
    SUBSCRIPTION_NAME = "data-canonization-started-log"
    SCHEMA = AvroSchema(schemas.EventDataCanonizationStarted)


class DataCanonizationCompletedConsumer(TopicConsumer, DataCanonizationMixin):
    TOPIC = topics.DATA_CANONIZATION_COMPLETED_V1_TOPIC
    SUBSCRIPTION_NAME = "data-canonization-completed-log"
    SCHEMA = AvroSchema(schemas.EventDataCanonizationCompleted)


CONSUMERS = [
    CreateDataIngestionConsumer,
    DataIngestionCreatedConsumer,
    DataIngestionStartedConsumer,
    DataIngestionFinishedConsumer,
    AnonimizationCompletedConsumer,
    CreateDataCanonizationConsumer,
    DataCanonizationCreatedConsumer,
    DataCanonizationStartedConsumer,
    DataCanonizationCompletedConsumer,
]
