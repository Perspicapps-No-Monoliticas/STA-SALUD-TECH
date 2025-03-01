from pulsar.schema import AvroSchema

from modules.data_canonization.infraestrucuture.repositories import (
    DataCanonizationSQLAlchemyRepository,
)
from modules.data_canonization.infraestrucuture.schema.v1.events import (
    EventDataCanonizationCreated,
    EventDataCanonizationCreatedPayload,
)
from modules.data_canonization.domain.events import (
    DataCanonizationStarted,
    # DataCanonizationUpdated,
)
from seedwork.infraestructure.dispatcher import Dispatcher, dispatch_event
from . import constants


class DataCanonizationCreatedDispatcher(Dispatcher):
    def handle(self, event: DataCanonizationStarted):
        data_canonization_dto = DataCanonizationSQLAlchemyRepository().get_by_id_raw(
            event.data_canonization_id
        )
        payload = EventDataCanonizationCreatedPayload(
            id=str(data_canonization_dto.id),
            provider_id=str(data_canonization_dto.provider_id),
            anonimization_id=str(data_canonization_dto.anonimization_id),
            ingestion_id=str(data_canonization_dto.ingestion_id),
            repository_in_path=data_canonization_dto.repository_in_path,
            created_at=data_canonization_dto.created_at.isoformat(),
            updated_at=data_canonization_dto.updated_at.isoformat(),
        )
        integration_event = EventDataCanonizationCreated(data=payload)
        self.publish_to_broker(
            message=integration_event,
            topic=constants.DATA_CANONIZATION_CREATED_V1_TOPIC,
            schema=AvroSchema(EventDataCanonizationCreated),
        )


@dispatch_event.register(DataCanonizationStarted)
def publish_data_canonization_started(event: DataCanonizationStarted):
    dispatcher = DataCanonizationCreatedDispatcher()
    dispatcher.handle(event)
