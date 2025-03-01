from dataclasses import dataclass
from typing import Type

from seedwork.domain.factories import Factory
from seedwork.domain.repositories import Repository
from seedwork.domain.exceptions import FactoryException
from modules.data_source.domain.repositories import DataSourceRepository
from .repositories import DataSourceSQLAlchemyRepository


@dataclass
class RepositoryFactory(Factory):
    def create_object(self, obj_type: Type, mapper=None) -> Repository:
        if obj_type == DataSourceRepository.__class__:
            return DataSourceSQLAlchemyRepository()
        raise FactoryException()
