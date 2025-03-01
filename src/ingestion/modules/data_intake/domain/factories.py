from dataclasses import dataclass

from seedwork.domain.factories import Factory
from seedwork.domain.repositories import Mapper
from seedwork.domain.entities import Entity
from .exceptions import ObjectTypeDoesNotExistInDataIntakeDomain
from .entities import DataIntake, IntakeStep


@dataclass
class _DataIntakeFactory(Factory):

    def create_object(self, obj: any, mapper: Mapper):

        if isinstance(obj, list):
            return [self.create_object(item, mapper) for item in obj]
        if isinstance(obj, Entity):
            return mapper.entity_to_dto(obj)
        if obj is None:
            return None
        data_intake: DataIntake = mapper.dto_to_entity(obj)
        # Check all required bussines rules

        return data_intake


@dataclass
class _DataIntakeStepFactory(Factory):

    def create_object(self, obj: any, mapper: Mapper):

        if isinstance(obj, list):
            return [self.create_object(item, mapper) for item in obj]
        if isinstance(obj, Entity):
            return mapper.entity_to_dto(obj)
        if obj is None:
            return None
        data_intake_step: IntakeStep = mapper.dto_to_entity(obj)
        # Check all required bussines rules

        return data_intake_step


@dataclass
class DataIntakeFactory(Factory):

    def create_object(self, obj: any, mapper: Mapper):
        if mapper.get_type() == DataIntake.__class__:
            data_source_factory = _DataIntakeFactory()
            return data_source_factory.create_object(obj, mapper)
        if mapper.get_type() == IntakeStep.__class__:
            intake_step_factory = _DataIntakeStepFactory()
            return intake_step_factory.create_object(obj, mapper)
        else:
            raise ObjectTypeDoesNotExistInDataIntakeDomain()
