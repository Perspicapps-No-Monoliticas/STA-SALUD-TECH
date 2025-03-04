from typing import Dict

from seedwork.application.dto import Mapper
from seedwork.domain.repositories import Mapper as RepMapper
from modules.data_intake.domain.entities import DataIntake, IntakeStep
from modules.data_intake.domain.value_objects import DataIntakeStatus, IntakeSpecs

from .dto import DataIntakeDTO, DataIntakeStepDTO
from .schemas import DataIntakeStepSchema, DataIntakeDetailSchema, IntakeInitSchema


class DataIntakeDTOJsonMapper(Mapper):
    def dto_to_external(self, dto: DataIntakeDTO) -> Dict:
        return DataIntakeDetailSchema(
            **{
                **dto.__dict__,
                "history": [DataIntakeStepSchema(**step) for step in dto.history],
            }
        ).model_dump()

    def external_to_dto(self, external: Dict) -> DataIntakeDTO:
        validated_data = DataIntakeDetailSchema(**external)
        data_source_dto = DataIntakeDTO(
            id=validated_data.id,
            created_at=validated_data.created_at,
            updated_at=validated_data.updated_at,
            provider_id=validated_data.provider_id,
            status=validated_data.status,
            total_records=validated_data.total_records,
            repository_out_path=validated_data.repository_out_path,
            history=[
                DataIntakeStepDTO(
                    id=step.id,
                    status=step.status,
                    created_at=step.created_at,
                    updated_at=step.updated_at,
                    data_source_id=step.data_source_id,
                    total_records=step.total_records,
                )
                for step in validated_data.history
            ],
        )

        return data_source_dto


class DataIntakeMapper(RepMapper):
    def entity_to_dto(self, entity: DataIntake) -> DataIntakeDTO:
        return DataIntakeDTO(
            id=entity.id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            provider_id=entity.provider_id,
            status=entity.status or DataIntakeStatus.CREATED,
            total_records=entity.specs.total_records or 0,
            repository_out_path=entity.specs.repository_out_path
            or f"{entity.provider_id}/ingestion/{entity.created_at}",
            history=[
                DataIntakeStepDTO(
                    id=step.id,
                    status=step.status,
                    created_at=step.created_at,
                    updated_at=step.updated_at,
                    data_source_id=step.data_source_id,
                    total_records=step.total_records,
                )
                for step in (entity.history or [])
            ],
        )

    def dto_to_entity(self, dto: DataIntakeDTO) -> DataIntake:
        return DataIntake(
            id=dto.id,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
            provider_id=dto.provider_id,
            status=dto.status,
            specs=IntakeSpecs(
                total_records=dto.total_records,
                repository_out_path=dto.repository_out_path,
            ),
            history=[
                IntakeStep(
                    id=step.id,
                    status=step.status,
                    created_at=step.created_at,
                    updated_at=step.updated_at,
                    data_source_id=step.data_source_id,
                    total_records=step.total_records,
                )
                for step in (dto.history or [])
            ],
        )

    def get_type(self) -> type:
        return DataIntake.__class__


class CreateIntakeDTOJsonMapper(Mapper):
    def external_to_dto(self, external: Dict) -> DataIntakeDTO:
        validated_data = IntakeInitSchema(**external)
        data_source_dto = DataIntakeDTO(
            provider_id=validated_data.provider_id,
            correlation_id=validated_data.correlation_id,
        )

        return data_source_dto

    def dto_to_external(self, dto: DataIntakeDTO) -> Dict:
        return IntakeInitSchema(provider_id=dto.provider_id).model_dump()
