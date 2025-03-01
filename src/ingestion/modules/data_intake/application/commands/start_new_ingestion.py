from dataclasses import dataclass
import uuid

from modules.data_intake.application.dto import DataIntakeDTO
from modules.data_intake.domain.entities import DataIntake
from modules.data_intake.application.mappers import DataIntakeMapper
from modules.data_intake.domain.repositories import DataIntakeRepository
from modules.data_intake.infrastructure.tasks import start_ingestion_task

from seedwork.application.commands import Command, execute_command
from seedwork.infrastructure.uow import UnitOfWorkPort
from .base import CreateDataIntakeBaseHandler


@dataclass
class StartDataIntakeCommand(Command):
    provider_id: uuid.UUID
    correlation_id: uuid.UUID

    @classmethod
    def from_dto(cls, dto: DataIntakeDTO):
        return cls(
            provider_id=dto.provider_id,
            correlation_id=dto.correlation_id,
        )

    def to_dto(self) -> DataIntakeDTO:
        return DataIntakeDTO(
            provider_id=self.provider_id,
            correlation_id=self.correlation_id,
        )


class StartDataIntakeCommandHandler(CreateDataIntakeBaseHandler):
    def handle(self, command: StartDataIntakeCommand):
        data_intake_dto = command.to_dto()
        data_intake: DataIntake = self.data_intake_factory.create_object(
            data_intake_dto, DataIntakeMapper()
        )
        data_intake.create_data_intake(data_intake, command.correlation_id)

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
        start_ingestion_task.delay(str(data_intake.id), str(command.correlation_id))


@execute_command.register(StartDataIntakeCommand)
def execute_create_data_intake(command: StartDataIntakeCommand):
    handler = StartDataIntakeCommandHandler()
    handler.handle(command)
