from typing import Type

from pulsar.schema import AvroSchema

from seedwork.infrastructure.schema.v1.events import IntegrationForCoreographyEvent
from seedwork.infrastructure.schema.v1.header import EventHeader
from .repositories import (
    DataIntakeSQLAlchemyRepository,
)
from .schema.v1.events import (
    DataIngestionCreated,
    DataIngestionStarted,
    DataIngestionFinished,
    DataIngestionPayload,
)
from modules.data_intake.domain.events import (
    DataintakeCreated,
    DataIntakeStarted,
    DataIntakeFinished,
)
from seedwork.infrastructure.dispatcher import Dispatcher, dispatch_event
from seedwork.infrastructure.varaibles import COUNTRY_CODE
from . import constants


class DataingestionEventDispatcher(Dispatcher):

    def __init__(self, schema: Type[IntegrationForCoreographyEvent], topic: str):
        super().__init__()
        self.schema = schema
        self.topic = topic

    def handle(
        self, event: DataintakeCreated | DataIngestionStarted | DataIngestionFinished
    ):
        data_intake_dto = DataIntakeSQLAlchemyRepository().get_by_id_raw(
            event.data_intake_id
        )
        payload = DataIngestionPayload(
            provider_id=str(data_intake_dto.provider_id),
            data_ingestion_id=str(data_intake_dto.id),
            status=data_intake_dto.status,
            repository_out_path=data_intake_dto.repository_out_path,
            country_iso=COUNTRY_CODE,
            created_at=data_intake_dto.created_at.isoformat(),
            updated_at=data_intake_dto.updated_at.isoformat(),
        )
        integration_event = self.schema(
            data=payload, header=EventHeader(correlation_id=str(event.correlation_id))
        )
        self.publish_to_broker(
            message=integration_event,
            topic=self.topic,
            schema=AvroSchema(self.schema),
        )


@dispatch_event.register(DataintakeCreated)
def publish_data_intake_created(event: DataintakeCreated):
    dispatcher = DataingestionEventDispatcher(
        DataIngestionCreated, constants.DATA_INGESTION_CREATED_V1_TOPIC
    )
    dispatcher.handle(event)


@dispatch_event.register(DataIntakeStarted)
def publish_data_intake_started(event: DataIntakeStarted):
    dispatcher = DataingestionEventDispatcher(
        DataIngestionStarted, constants.DATA_INGESTION_STARTED_V1_TOPIC
    )
    dispatcher.handle(event)


@dispatch_event.register(DataIntakeFinished)
def publish_data_intake_finished(event: DataIntakeFinished):
    dispatcher = DataingestionEventDispatcher(
        DataIngestionFinished, constants.DATA_INGESTION_FINISHED_V1_TOPIC
    )
    dispatcher.handle(event)
