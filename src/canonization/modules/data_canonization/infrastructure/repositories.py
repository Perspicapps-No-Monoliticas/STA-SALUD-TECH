from modules.data_canonization.domain.repositories import (
    DataCanonizationRepository,
    DataCanonizationStepRepository,
)
from modules.data_canonization.domain.factories import DataCanonizationFactory
from modules.data_canonization.domain import entities as domain_entities
from seedwork.infrastructure.repositories import SQLAlchemyRepository
from .dto import (
    DataCanonization as DataCanonizationDTO,
    DataCanonizationStep as DataCanonizationStepDTO,
)
from .mappers import DataCanonizationMapper, DataCanonizationStepMapper


class DataCanonizationSQLAlchemyRepository(
    DataCanonizationRepository,
    SQLAlchemyRepository[DataCanonizationDTO, domain_entities.DataCanonization],
):
    def __init__(self):
        super().__init__(
            DataCanonizationFactory, DataCanonizationMapper, DataCanonizationDTO
        )


class DataCanonizationStepSQLAlchemyRepository(
    DataCanonizationStepRepository,
    SQLAlchemyRepository[DataCanonizationStepDTO, domain_entities.CanonizationStep],
):
    def __init__(self):
        super().__init__(
            DataCanonizationFactory, DataCanonizationStepMapper, DataCanonizationStepDTO
        )
