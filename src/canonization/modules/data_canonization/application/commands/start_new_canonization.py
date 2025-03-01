from dataclasses import dataclass
import uuid

from modules.data_canonization.application.dto import DataCanonizationDTO
from modules.data_canonization.domain.entities import DataCanonization
from modules.data_canonization.application.mappers import DataCanonizationMapper
from modules.data_canonization.domain.repositories import DataCanonizationRepository

from seedwork.application.commands import Command, execute_command
from seedwork.infraestructure.uow import UnitOfWorkPort
from .base import CreateDataCanonizationBaseHandler


@dataclass
class StartDataCanonizationCommand(Command):
    provider_id: uuid.UUID
    anonimization_id: uuid.UUID
    ingestion_id: uuid.UUID
    repository_in_path: str

    @classmethod
    def from_dto(cls, dto: DataCanonizationDTO):
        return cls(
            provider_id=dto.provider_id,
            anonimization_id=dto.anonimization_id,
            ingestion_id=dto.ingestion_id,
            repository_in_path=dto.repository_in_path,
        )

    def to_dto(self) -> DataCanonizationDTO:
        return DataCanonizationDTO(
            provider_id=self.provider_id,
            anonimization_id=self.anonimization_id,
            ingestion_id=self.ingestion_id,
            repository_in_path=self.repository_in_path,
        )


class StartDataCanonizationCommandHandler(CreateDataCanonizationBaseHandler):
    def handle(self, command: StartDataCanonizationCommand):
        data_canonization_dto = command.to_dto()
        data_canonization: DataCanonization = (
            self.data_canonization_factory.create_object(
                data_canonization_dto, DataCanonizationMapper()
            )
        )
        data_canonization.create_data_canonization(data_canonization)

        repository = self.repository_factory.create_object(
            DataCanonizationRepository.__class__
        )
        UnitOfWorkPort.register_batch(repository.add, data_canonization)
        try:
            UnitOfWorkPort.savepoint()
            UnitOfWorkPort.commit()
            print(f"Data intake {data_canonization.id} created")
        except Exception as e:
            UnitOfWorkPort.rollback()
            raise e
        # TODO: Should trigger a celery taks or something similar


@execute_command.register(StartDataCanonizationCommand)
def execute_create_data_canonization(command: StartDataCanonizationCommand):
    handler = StartDataCanonizationCommandHandler()
    handler.handle(command)
