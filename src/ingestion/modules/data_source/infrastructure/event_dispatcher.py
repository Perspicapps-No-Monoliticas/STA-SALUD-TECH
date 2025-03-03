from pulsar.schema import AvroSchema

from modules.data_source.infrastructure.repositories import (
    DataSourceSQLAlchemyRepository,
)
from modules.data_source.infrastructure.schema.v1.events import (
    EventDataSourceCreated,
    CredentialsPayload,
    EventDataSourceCreatedPayload,
)
from modules.data_source.domain.events import (
    DataSourceCreated,
    DataSourceUpdated,
)
from seedwork.infrastructure.dispatcher import Dispatcher, dispatch_event
from . import constants


class DataSourceCreatedDispatcher(Dispatcher):
    def handle(self, event: DataSourceCreated):
        data_source_dto = DataSourceSQLAlchemyRepository().get_by_id_raw(
            event.data_source_id
        )
        payload = EventDataSourceCreatedPayload(
            name=data_source_dto.name,
            description=data_source_dto.description,
            type=data_source_dto.type,
            credentials=CredentialsPayload(
                payload=data_source_dto.credentials.get("payload"),
                type=data_source_dto.credentials.get("type"),
            ),
            provider_id=str(data_source_dto.provider_id),
            id=str(data_source_dto.id),
            created_at=data_source_dto.created_at.isoformat(),
            updated_at=data_source_dto.updated_at.isoformat(),
        )
        integration_event = EventDataSourceCreated(data=payload)
        self.publish_to_broker(
            message=integration_event,
            topic=constants.DATA_SOURCE_CREATED_V1_TOPIC,
            schema=AvroSchema(EventDataSourceCreated),
        )


@dispatch_event.register(DataSourceCreated)
def publish_data_source_created(event: DataSourceCreated):
    dispatcher = DataSourceCreatedDispatcher()
    dispatcher.handle(event)
