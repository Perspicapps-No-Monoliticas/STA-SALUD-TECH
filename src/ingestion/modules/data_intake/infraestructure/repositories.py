from modules.data_intake.domain.repositories import (
    DataIntakeRepository,
    DataIntakeStepRepository,
)
from modules.data_intake.domain.factories import DataIntakeFactory
from modules.data_intake.domain import entities as domain_entities
from seedwork.infraestructure.repositories import SQLAlchemyRepository
from .dto import DataIntake as DataIntakeDTO, DataIntakeStep as DataIntakeStepDTO
from .mappers import DataIntakeMapper, DataIntakeStepMapper


class DataIntakeSQLAlchemyRepository(
    DataIntakeRepository,
    SQLAlchemyRepository[DataIntakeDTO, domain_entities.DataIntake],
):
    def __init__(self):
        super().__init__(DataIntakeFactory, DataIntakeMapper, DataIntakeDTO)


class DataIntakeStepSQLAlchemyRepository(
    DataIntakeStepRepository,
    SQLAlchemyRepository[DataIntakeStepDTO, domain_entities.IntakeStep],
):
    def __init__(self):
        super().__init__(DataIntakeFactory, DataIntakeStepMapper, DataIntakeStepDTO)
