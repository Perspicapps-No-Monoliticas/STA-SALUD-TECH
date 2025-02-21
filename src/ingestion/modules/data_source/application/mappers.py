from typing import Dict

from seedwork.application.dto import Mapper
from .dto import DataSourceDTO
from .schemas import DataSourceCreationSchema, DataSourceDetailSchema


class MapperDataSourceDTOJson(Mapper):

    def dto_to_external(self, dto: DataSourceDTO) -> Dict:
        return DataSourceDetailSchema(**dto.__dict__).model_dump()

    def external_to_dto(self, external: Dict) -> DataSourceDTO:
        validated_data = DataSourceCreationSchema(**external)
        data_source_dto = DataSourceDTO(
            name=validated_data.name,
            description=validated_data.description,
            type=validated_data.type.value,
            credentials=validated_data.credentials,
            provider_id=validated_data.provider_id,
        )

        return data_source_dto
