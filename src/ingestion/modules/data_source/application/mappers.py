from typing import Dict

from seedwork.application.dto import Mapper
from seedwork.domain.repositories import Mapper as RepMapper
from modules.data_source.domain.entities import DataSource
from modules.data_source.domain.value_objects import (
    Credentials,
    Information,
    DataSourceType,
    CredentialType,
)
from .dto import DataSourceDTO, CredentialsDTO
from .schemas import DataSourceCreationSchema, DataSourceDetailSchema


class MapperDataSourceDTOJson(Mapper):

    def dto_to_external(self, dto: DataSourceDTO) -> Dict:
        return DataSourceDetailSchema(
            **{**dto.__dict__, "credentials": dto.credentials.__dict__}
        ).model_dump()

    def external_to_dto(self, external: Dict) -> DataSourceDTO:
        validated_data = DataSourceCreationSchema(**external)
        data_source_dto = DataSourceDTO(
            name=validated_data.name,
            description=validated_data.description,
            type=validated_data.type.value,
            credentials=CredentialsDTO(
                payload=validated_data.credentials.payload,
                type=validated_data.credentials.type,
            ),
            provider_id=validated_data.provider_id,
        )

        return data_source_dto


class DataSourceMapper(RepMapper):

    def get_type(self):
        return DataSource.__class__

    def entity_to_dto(self, entity: DataSource) -> DataSourceDTO:
        return DataSourceDTO(
            name=entity.infromation.name,
            description=entity.infromation.description,
            type=entity.type.value,
            credentials=CredentialsDTO(
                payload=entity.credentials.payload,
                type=entity.credentials.type.value,
            ),
            provider_id=entity.provider_id,
        )

    def dto_to_entity(self, dto: DataSourceDTO) -> DataSource:
        return DataSource(
            infromation=Information(name=dto.name, description=dto.description),
            type=DataSourceType(dto.type),
            credentials=Credentials(
                payload=dto.credentials.payload,
                type=CredentialType(dto.credentials.type),
            ),
            provider_id=dto.provider_id,
        )
