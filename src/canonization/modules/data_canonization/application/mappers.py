from typing import Dict

from seedwork.application.dto import Mapper
from seedwork.domain.repositories import Mapper as RepMapper
from modules.data_canonization.domain.entities import DataCanonization, IntakeStep
from modules.data_canonization.domain.value_objects import (
    DataCanonizationStatus,
    IntakeSpecs,
)

from .dto import DataCanonizationDTO, DataCanonizationStepDTO
from .schemas import (
    DataCanonizationStepSchema,
    DataCanonizationDetailSchema,
    IntakeInitSchema,
)


class DataCanonizationDTOJsonMapper(Mapper):
    def dto_to_external(self, dto: DataCanonizationDTO) -> Dict:
        return DataCanonizationDetailSchema(
            **{
                **dto.__dict__,
                "steps": [DataCanonizationStepSchema(**step) for step in dto.steps],
            }
        ).model_dump()

    def external_to_dto(self, external: Dict) -> DataCanonizationDTO:
        validated_data = DataCanonizationDetailSchema(**external)
        data_canonization_dto = DataCanonizationDTO(
            id=validated_data.id,
            created_at=validated_data.created_at,
            updated_at=validated_data.updated_at,
            provider_id=validated_data.provider_id,
            status=validated_data.status,
            total_records=validated_data.total_records,
            repository_in_path=validated_data.repository_in_path,
            history=[
                DataCanonizationStepDTO(
                    id=step.id,
                    status=step.status,
                    created_at=step.created_at,
                    updated_at=step.updated_at,
                    total_records=step.total_records,
                )
                for step in validated_data.history
            ],
        )

        return data_canonization_dto


class DataCanonizationMapper(RepMapper):
    def entity_to_dto(self, entity: DataCanonization) -> DataCanonizationDTO:
        return DataCanonizationDTO(
            id=entity.id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            provider_id=entity.provider_id,
            anonimization_id=entity.anonimization_id,
            ingestion_id=entity.ingestion_id,
            status=entity.status or DataCanonizationStatus.CREATED,
            total_records=entity.specs.total_records or 0,
            repository_in_path=entity.specs.repository_in_path
            or f"{entity.provider_id}/ingestion/{entity.created_at}",
            steps=[
                DataCanonizationStepDTO(
                    id=step.id,
                    status=step.status,
                    created_at=step.created_at,
                    updated_at=step.updated_at,
                    total_records=step.total_records,
                    ai_model_id=step.ai_model_id,
                    data_canonization_id=step.data_canonization_id,
                )
                for step in (entity.steps or [])
            ],
        )

    def dto_to_entity(self, dto: DataCanonizationDTO) -> DataCanonization:
        return DataCanonization(
            id=dto.id,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
            provider_id=dto.provider_id,
            anonimization_id=dto.anonimization_id,
            ingestion_id=dto.ingestion_id,
            status=dto.status,
            specs=IntakeSpecs(
                total_records=dto.total_records,
                repository_in_path=dto.repository_in_path,
            ),
            steps=[
                IntakeStep(
                    id=step.id,
                    status=step.status,
                    created_at=step.created_at,
                    updated_at=step.updated_at,
                    total_records=step.total_records,
                    ai_model_id=step.ai_model_id,
                    data_canonization_id=step.data_canonization_id,
                )
                for step in (dto.steps or [])
            ],
        )

    def get_type(self) -> type:
        return DataCanonization.__class__


class CreateIntakeDTOJsonMapper(Mapper):
    def external_to_dto(self, external: Dict) -> DataCanonizationDTO:
        validated_data = IntakeInitSchema(**external)
        data_canonization_dto = DataCanonizationDTO(
            provider_id=validated_data.provider_id,
            anonimization_id=validated_data.anonimization_id,
            ingestion_id=validated_data.ingestion_id,
            repository_in_path=validated_data.repository_in_path,
        )

        return data_canonization_dto

    def dto_to_external(self, dto: DataCanonizationDTO) -> Dict:
        return IntakeInitSchema(
            provider_id=dto.provider_id,
            anonimization_id=dto.anonimization_id,
            ingestion_id=dto.ingestion_id,
            repository_in_path=dto.repository_in_path,
        ).model_dump()
