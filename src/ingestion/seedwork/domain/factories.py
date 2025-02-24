from abc import ABC, abstractmethod
from .mixins import RuleValidationMixin
from .repositories import Mapper


class Factory(ABC, RuleValidationMixin):
    @abstractmethod
    def create_object(self, obj: any, mapper: Mapper = None) -> any: ...
