from dataclasses import dataclass
from typing import Type

from seedwork.domain.factories import Factory
from seedwork.domain.repositories import Repository
from seedwork.domain.exceptions import FactoryException
from modules.data_intake.domain.repositories import (
    DataIntakeRepository,
    DataIntakeStepRepository,
)
from .repositories import (
    DataIntakeSQLAlchemyRepository,
    DataIntakeStepSQLAlchemyRepository,
)


@dataclass
class RepositoryFactory(Factory):
    def create_object(self, obj_type: Type, mapper=None) -> Repository:
        if obj_type == DataIntakeRepository.__class__:
            return DataIntakeSQLAlchemyRepository()
        if obj_type == DataIntakeStepRepository.__class__:
            return DataIntakeStepSQLAlchemyRepository()
        raise FactoryException()
