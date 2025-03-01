from dataclasses import dataclass

from seedwork.domain.factories import Factory
from seedwork.domain.repositories import Mapper
from seedwork.domain.entities import Entity
from .exceptions import ObjectTypeDoesNotExistInDataCanonizationDomain
from .entities import DataCanonization, CanonizationStep


@dataclass
class _DataCanonizationFactory(Factory):

    def create_object(self, obj: any, mapper: Mapper):

        if isinstance(obj, list):
            return [self.create_object(item, mapper) for item in obj]
        if isinstance(obj, Entity):
            return mapper.entity_to_dto(obj)
        if obj is None:
            return None
        data_canonization: DataCanonization = mapper.dto_to_entity(obj)
        # Check all required bussines rules

        return data_canonization


@dataclass
class _DataCanonizationStepFactory(Factory):

    def create_object(self, obj: any, mapper: Mapper):

        if isinstance(obj, list):
            return [self.create_object(item, mapper) for item in obj]
        if isinstance(obj, Entity):
            return mapper.entity_to_dto(obj)
        if obj is None:
            return None
        data_canonization_step: CanonizationStep = mapper.dto_to_entity(obj)
        # Check all required bussines rules

        return data_canonization_step


@dataclass
class DataCanonizationFactory(Factory):

    def create_object(self, obj: any, mapper: Mapper):
        if mapper.get_type() == DataCanonization.__class__:
            data_canonization_factory = _DataCanonizationFactory()
            return data_canonization_factory.create_object(obj, mapper)
        if mapper.get_type() == CanonizationStep.__class__:
            canonization_step_factory = _DataCanonizationStepFactory()
            return canonization_step_factory.create_object(obj, mapper)
        else:
            raise ObjectTypeDoesNotExistInDataCanonizationDomain()
