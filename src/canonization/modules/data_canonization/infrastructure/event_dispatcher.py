from typing import Type

from pulsar.schema import AvroSchema, Record

from .repositories import (
    DataCanonizationSQLAlchemyRepository,
)
from .schema.v1.events import (
    EventDataCanonizationCreated,
    EventDataCanonizationStarted,
    EventDataCanonizationCompleted,
    DataCanonizationPayload,
)
from modules.data_canonization.domain.events import (
    DataCanonizationCreated,
    DataCanonizationStarted,
    DataCanonizationFinished,
)
from seedwork.infrastructure.dispatcher import Dispatcher, dispatch_event
from seedwork.infrastructure.varaibles import COUNTRY_CODE
from seedwork.infrastructure.schema.v1.header import EventHeader
from . import constants


class DatacanonizationEventDispatcher(Dispatcher):

    def __init__(self, schema: Type[Record], topic: str):
        super().__init__()
        self.schema = schema
        self.topic = topic

    def handle(
        self,
        event: (
            DataCanonizationCreated | DataCanonizationStarted | DataCanonizationFinished
        ),
    ):
        data_canonization_dto = DataCanonizationSQLAlchemyRepository().get_by_id_raw(
            event.data_canonization_id
        )
        payload = DataCanonizationPayload(
            data_canonization_id=str(data_canonization_dto.id),
            provider_id=str(data_canonization_dto.provider_id),
            anonimization_id=str(data_canonization_dto.anonimization_id),
            ingestion_id=str(data_canonization_dto.ingestion_id),
            repository_in_path=data_canonization_dto.repository_in_path,
            status=data_canonization_dto.status,
            country_iso=COUNTRY_CODE,
            created_at=data_canonization_dto.created_at.isoformat(),
            updated_at=data_canonization_dto.updated_at.isoformat(),
        )
        header = EventHeader(corellation_id=event.correlation_id)
        integration_event = self.schema(
            data=payload,
            header=header,
        )
        self.publish_to_broker(
            message=integration_event,
            topic=self.topic,
            schema=AvroSchema(self.schema),
        )


@dispatch_event.register(DataCanonizationCreated)
def publish_data_canonization_created(event: DataCanonizationCreated):
    dispatcher = DatacanonizationEventDispatcher(
        EventDataCanonizationCreated, constants.DATA_CANONIZATION_CREATED_V1_TOPIC
    )
    dispatcher.handle(event)


@dispatch_event.register(DataCanonizationStarted)
def publish_data_canonization_started(event: DataCanonizationStarted):
    dispatcher = DatacanonizationEventDispatcher(
        EventDataCanonizationStarted, constants.DATA_CANONIZATION_STARTED_V1_TOPIC
    )
    dispatcher.handle(event)


@dispatch_event.register(DataCanonizationFinished)
def publish_data_canonization_finished(event: DataCanonizationFinished):
    dispatcher = DatacanonizationEventDispatcher(
        EventDataCanonizationCompleted, constants.DATA_CANONIZATION_COMPLETED_V1_TOPIC
    )
    dispatcher.handle(event)
