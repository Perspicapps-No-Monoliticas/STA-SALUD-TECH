from dataclasses import dataclass
import uuid

from modules.data_intake.application.dto import DataIntakeDTO
from modules.data_intake.domain.entities import DataIntake
from modules.data_intake.application.mappers import DataIntakeMapper
from modules.data_intake.domain.repositories import DataIntakeRepository

from seedwork.application.commands import Command, execute_command
from seedwork.infraestructure.uow import UnitOfWorkPort
from .base import CreateDataIntakeBaseHandler


@dataclass
class StartDataIntakeCommand(Command):
    provider_id: uuid.UUID

    @classmethod
    def from_dto(cls, dto: DataIntakeDTO):
        return cls(
            provider_id=dto.provider_id,
        )

    def to_dto(self) -> DataIntakeDTO:
        return DataIntakeDTO(
            provider_id=self.provider_id,
        )


class StartDataIntakeCommandHandler(CreateDataIntakeBaseHandler):
    def handle(self, command: StartDataIntakeCommand):
        data_intake_dto = command.to_dto()
        data_intake: DataIntake = self.data_intake_factory.create_object(
            data_intake_dto, DataIntakeMapper()
        )
        data_intake.create_data_intake(data_intake)

        repository = self.repository_factory.create_object(
            DataIntakeRepository.__class__
        )
        UnitOfWorkPort.register_batch(repository.add, data_intake)
        try:
            UnitOfWorkPort.savepoint()
            UnitOfWorkPort.commit()
            print(f"Data intake {data_intake.id} created")
        except Exception as e:
            UnitOfWorkPort.rollback()
            raise e
        # TODO: Should trigger a celery taks or something similar


@execute_command.register(StartDataIntakeCommand)
def execute_create_data_intake(command: StartDataIntakeCommand):
    handler = StartDataIntakeCommandHandler()
    handler.handle(command)
