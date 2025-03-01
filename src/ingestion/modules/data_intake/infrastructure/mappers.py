from modules.data_intake.domain.entities import DataIntake, IntakeStep
from modules.data_intake.domain.value_objects import IntakeSpecs
from seedwork.domain.repositories import Mapper
from .dto import DataIntake as DataIntakeDTO, DataIntakeStep as DataIntakeStepDTO


class DataIntakeMapper(Mapper):
    def entity_to_dto(self, entity: DataIntake) -> DataIntakeDTO:
        return DataIntakeDTO(
            id=entity.id,
            provider_id=entity.provider_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            status=entity.status,
            total_records=entity.specs.total_records,
            repository_out_path=entity.specs.repository_out_path,
        )

    def dto_to_entity(self, dto: DataIntakeDTO) -> DataIntake:
        return DataIntake(
            id=dto.id,
            provider_id=dto.provider_id,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
            status=dto.status,
            specs=IntakeSpecs(
                total_records=dto.total_records,
                repository_out_path=dto.repository_out_path,
            ),
            history=[
                IntakeStep(
                    id=step.id,
                    created_at=step.created_at,
                    updated_at=step.updated_at,
                    status=step.status,
                    data_source_id=step.data_source_id,
                    total_records=step.total_records,
                )
                for step in (dto.history or [])
            ],
        )

    def get_type(self) -> type:
        return DataIntake.__class__


class DataIntakeStepMapper(Mapper):
    def get_type(self) -> type:
        return IntakeStep.__class__

    def entity_to_dto(self, entity: IntakeStep) -> DataIntakeStepDTO:
        return DataIntakeStepDTO(
            id=entity.id,
            data_source_id=entity.data_source_id,
            data_intake_id=entity.data_intake_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            status=entity.status,
            total_records=entity.total_records,
        )

    def dto_to_entity(self, dto: DataIntakeStepDTO) -> IntakeStep:
        return IntakeStep(
            id=dto.id,
            data_source_id=dto.data_source_id,
            data_intake_id=dto.data_intake_id,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
            status=dto.status,
            total_records=dto.total_records,
        )
