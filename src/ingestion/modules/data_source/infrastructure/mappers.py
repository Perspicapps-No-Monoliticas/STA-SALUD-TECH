from seedwork.domain.repositories import Mapper

from modules.data_source.domain.entities import DataSource

from modules.data_source.domain.value_objects import (
    Credentials,
    Information,
    DataSourceType,
    CredentialType,
)
from .dto import DataSource as DataSourceDTO


class DataSourceMapper(Mapper):

    def get_type(self) -> type:
        return DataSource.__class__

    def entity_to_dto(self, entity: DataSource) -> DataSourceDTO:
        return DataSourceDTO(
            id=entity.id,
            name=entity.infromation.name,
            description=entity.infromation.description,
            type=entity.type.value,
            credentials={
                "type": entity.credentials.type.value,
                "payload": entity.credentials.payload,
            },
            provider_id=entity.provider_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def dto_to_entity(self, dto: DataSourceDTO) -> DataSource:
        return DataSource(
            id=dto.id,
            infromation=Information(
                name=dto.name,
                description=dto.description,
            ),
            type=DataSourceType(dto.type),
            credentials=Credentials(
                payload=dto.credentials.get("payload"),
                type=CredentialType(dto.credentials.get("type")),
            ),
            provider_id=dto.provider_id,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )
