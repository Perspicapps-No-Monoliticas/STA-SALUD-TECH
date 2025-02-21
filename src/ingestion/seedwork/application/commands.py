from functools import singledispatch
from abc import ABC, abstractmethod


class Command: ...


class CommandHandler(ABC):
    @abstractmethod
    def handle(self, command: Command):
        raise NotImplementedError()


@singledispatch
def execute_command(command):
    raise NotImplementedError(f"No handler for command {type(command).__name__}")
