import uuid
from typing import Optional

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
from sqlalchemy.orm import Query
from .mappers import DataCanonizationMapper, DataCanonizationStepMapper


class DataCanonizationSQLAlchemyRepository(
    DataCanonizationRepository,
    SQLAlchemyRepository[DataCanonizationDTO, domain_entities.DataCanonization],
):
    def __init__(self):
        super().__init__(
            DataCanonizationFactory, DataCanonizationMapper, DataCanonizationDTO
        )

    def get_paginated(
        self,
        page,
        per_page,
        provider_id: Optional[uuid.UUID] = None,
        ingestion_id: Optional[uuid.UUID] = None,
    ):

        def filter_query(query: Query):
            if provider_id:
                query = query.filter(DataCanonizationDTO.provider_id == provider_id)
            if ingestion_id:
                query = query.filter(DataCanonizationDTO.ingestion_id == ingestion_id)
            return query

        return super().get_paginated(page, per_page, extra_q=filter_query)


class DataCanonizationStepSQLAlchemyRepository(
    DataCanonizationStepRepository,
    SQLAlchemyRepository[DataCanonizationStepDTO, domain_entities.CanonizationStep],
):
    def __init__(self):
        super().__init__(
            DataCanonizationFactory, DataCanonizationStepMapper, DataCanonizationStepDTO
        )
