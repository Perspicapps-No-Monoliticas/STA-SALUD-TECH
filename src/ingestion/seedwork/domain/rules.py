from abc import ABC, abstractmethod


class BussinessRule(ABC):
    __message: str = "Invalid bussines rule"

    def __init__(self, message):
        self.__message = message

    @property
    def error_message(self) -> str:
        return self.__message

    @abstractmethod
    def is_valid(self) -> bool: ...

    def __str__(self):
        return f"{self.__class__.__name__} - {self.__message}"


class InmitableEntity(BussinessRule):

    entity: object

    def __init__(self, entity, message="If should be inmutable"):
        super().__init__(message)
        self.entity = entity

    def is_valid(self) -> bool:
        try:
            if self.entity._id:
                return False
        except AttributeError:
            return True
