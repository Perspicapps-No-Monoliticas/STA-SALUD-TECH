from pulsar.schema import AvroSchema

from seedwork.infraestructure.schema.v1.events import IntegrationEvent
from seedwork.domain.events import DomainEvent
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
from seedwork.infraestructure.dispatcher import Dispatcher, dispatch_event
from seedwork.infraestructure.varaibles import COUNTRY_CODE
from . import constants


class DataSourceCreatedDispatcher(Dispatcher):

    def __init__(self, schema: IntegrationEvent):
        super().__init__()
        self.schema = schema

    def handle(self, event: DomainEvent):
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
        integration_event = DataIngestionCreated(
            data=payload,
            coreography_id=event.coreography_id,
        )
        self.publish_to_broker(
            message=integration_event,
            topic=constants.DATA_INGESTION_CREATED_V1_TOPIC,
            schema=AvroSchema(DataIngestionCreated),
        )


@dispatch_event.register(DataintakeCreated)
def publish_data_intake_created(event: DataintakeCreated):
    dispatcher = DataSourceCreatedDispatcher()
    dispatcher.handle(event)


@dispatch_event.register(DataIntakeStarted)
def publish_data_intake_started(event: DataIntakeStarted):
    dispatcher = DataSourceCreatedDispatcher()
    dispatcher.handle(event)


@dispatch_event.register(DataIntakeFinished)
def publish_data_intake_finished(event: DataIntakeFinished):
    dispatcher = DataSourceCreatedDispatcher()
    dispatcher.handle(event)
