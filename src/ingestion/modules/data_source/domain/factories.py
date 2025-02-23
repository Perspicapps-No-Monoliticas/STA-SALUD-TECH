from dataclasses import dataclass

from seedwork.domain.factories import Factory
from seedwork.domain.repositories import Mapper
from seedwork.domain.entities import Entity
from .entities import DataSource
from .exceptions import ObjectTypeDoesNotExistInDataSourceDomain
from .rules import HasCredentials, ValidDataSourceType


@dataclass
class _DataSourceFactory(Factory):

    def create_object(self, obj: any, mapper: Mapper):
        if not obj:
            return None
        if isinstance(obj, list):
            return [self.create_object(item, mapper) for item in obj]
        if isinstance(obj, Entity):
            return mapper.entity_to_dto(obj)
        data_source: DataSource = mapper.dto_to_entity(obj)
        # Check all required bussines rules
        self.check_rule(HasCredentials(data_source.credentials))
        self.check_rule(ValidDataSourceType(data_source.type))
        return data_source


@dataclass
class DataSourceFactory(Factory):

    def create_object(self, obj: any, mapper: Mapper):
        if mapper.get_type() == DataSource.__class__:
            data_source_factory = _DataSourceFactory()
            return data_source_factory.create_object(obj, mapper)
        else:
            raise ObjectTypeDoesNotExistInDataSourceDomain()
