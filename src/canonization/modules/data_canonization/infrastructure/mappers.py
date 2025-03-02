from modules.data_canonization.domain.entities import DataCanonization, CanonizationStep
from modules.data_canonization.domain.value_objects import CanonizationSpecs
from seedwork.domain.repositories import Mapper
from .dto import (
    DataCanonization as DataCanonizationDTO,
    DataCanonizationStep as DataCanonizationStepDTO,
)


class DataCanonizationMapper(Mapper):
    def entity_to_dto(self, entity: DataCanonization) -> DataCanonizationDTO:
        return DataCanonizationDTO(
            id=entity.id,
            provider_id=entity.provider_id,
            anonimization_id=entity.anonimization_id,
            ingestion_id=entity.ingestion_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            status=entity.status,
            total_records=entity.specs.total_records,
            repository_in_path=entity.specs.repository_in_path,
            steps=[
                DataCanonizationStepDTO(
                    id=step.id,
                    created_at=step.created_at,
                    updated_at=step.updated_at,
                    status=step.status,
                    total_records=step.total_records,
                    data_canonization_id=step.data_canonization_id,
                    ai_model_id=step.ai_model_id,
                )
                for step in entity.steps
            ],
        )

    def dto_to_entity(self, dto: DataCanonizationDTO) -> DataCanonization:
        return DataCanonization(
            id=dto.id,
            provider_id=dto.provider_id,
            anonimization_id=dto.anonimization_id,
            ingestion_id=dto.ingestion_id,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
            status=dto.status,
            specs=CanonizationSpecs(
                total_records=dto.total_records,
                repository_in_path=dto.repository_in_path,
            ),
            steps=[
                CanonizationStep(
                    id=step.id,
                    created_at=step.created_at,
                    updated_at=step.updated_at,
                    status=step.status,
                    total_records=step.total_records,
                    data_canonization_id=step.data_canonization_id,
                    ai_model_id=step.ai_model_id,
                )
                for step in (dto.steps or [])
            ],
        )

    def get_type(self) -> type:
        return DataCanonization.__class__


class DataCanonizationStepMapper(Mapper):
    def get_type(self) -> type:
        return CanonizationStep.__class__

    def entity_to_dto(self, entity: CanonizationStep) -> DataCanonizationStepDTO:
        return DataCanonizationStepDTO(
            id=entity.id,
            data_canonization_id=entity.data_canonization_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            status=entity.status,
            total_records=entity.total_records,
        )

    def dto_to_entity(self, dto: DataCanonizationStepDTO) -> CanonizationStep:
        return CanonizationStep(
            id=dto.id,
            data_canonization_id=dto.data_canonization_id,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
            status=dto.status,
            total_records=dto.total_records,
        )
