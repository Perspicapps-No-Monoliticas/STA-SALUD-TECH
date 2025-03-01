from dataclasses import dataclass
from typing import Type

from seedwork.domain.factories import Factory
from seedwork.domain.repositories import Repository
from seedwork.domain.exceptions import FactoryException
from modules.data_canonization.domain.repositories import (
    DataCanonizationRepository,
    DataCanonizationStepRepository,
)
from .repositories import (
    DataCanonizationSQLAlchemyRepository,
    DataCanonizationStepSQLAlchemyRepository,
)


@dataclass
class RepositoryFactory(Factory):
    def create_object(self, obj_type: Type, mapper=None) -> Repository:
        if obj_type == DataCanonizationRepository.__class__:
            return DataCanonizationSQLAlchemyRepository()
        if obj_type == DataCanonizationStepRepository.__class__:
            return DataCanonizationStepSQLAlchemyRepository()
        raise FactoryException()
