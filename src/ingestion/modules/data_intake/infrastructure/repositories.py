import uuid
from sqlalchemy.orm import Query

from modules.data_intake.domain.repositories import (
    DataIntakeRepository,
    DataIntakeStepRepository,
)
from modules.data_intake.domain.factories import DataIntakeFactory
from modules.data_intake.domain import entities as domain_entities
from seedwork.infrastructure.repositories import SQLAlchemyRepository
from .dto import DataIntake as DataIntakeDTO, DataIntakeStep as DataIntakeStepDTO
from .mappers import DataIntakeMapper, DataIntakeStepMapper


class DataIntakeSQLAlchemyRepository(
    DataIntakeRepository,
    SQLAlchemyRepository[DataIntakeDTO, domain_entities.DataIntake],
):
    def __init__(self):
        super().__init__(DataIntakeFactory, DataIntakeMapper, DataIntakeDTO)

    def get_paginated(self, page, per_page, provider_id: uuid.UUID = None):
        def extra_query(query: Query) -> Query:
            if not provider_id:
                return query
            return query.filter(DataIntakeDTO.provider_id == provider_id)

        return super().get_paginated(page, per_page, extra_q=extra_query)


class DataIntakeStepSQLAlchemyRepository(
    DataIntakeStepRepository,
    SQLAlchemyRepository[DataIntakeStepDTO, domain_entities.IntakeStep],
):
    def __init__(self):
        super().__init__(DataIntakeFactory, DataIntakeStepMapper, DataIntakeStepDTO)
