from dataclasses import dataclass
import uuid

from modules.data_source.application.dto import CredentialsDTO, DataSourceDTO
from modules.data_source.domain.entities import DataSource
from modules.data_source.application.mappers import DataSourceMapper
from modules.data_source.domain.repositories import DataSourceRepository

from seedwork.application.commands import Command, execute_command
from seedwork.infraestructure.uow import UnitOfWorkPort
from .base import CreateDataSourceBaseHandler


@dataclass
class CreateDataSource(Command):
    name: str
    description: str
    type: str
    credentials: CredentialsDTO
    provider_id: uuid.UUID

    @classmethod
    def from_dto(cls, dto: DataSourceDTO):
        return cls(
            name=dto.name,
            description=dto.description,
            type=dto.type,
            credentials=dto.credentials,
            provider_id=dto.provider_id,
        )

    def to_dto(self) -> DataSourceDTO:
        return DataSourceDTO(
            name=self.name,
            description=self.description,
            type=self.type,
            credentials=self.credentials,
            provider_id=self.provider_id,
        )


class CreateDataSourceCommandHandler(CreateDataSourceBaseHandler):
    def handle(self, command: CreateDataSource):
        data_source_dto = command.to_dto()
        data_source: DataSource = self.data_source_factory.create_object(
            data_source_dto, DataSourceMapper()
        )
        data_source.create_data_source(data_source)

        repository = self.repository_factory.create_object(
            DataSourceRepository.__class__
        )
        UnitOfWorkPort.register_batch(repository.add, data_source)
        try:
            UnitOfWorkPort.savepoint()
            UnitOfWorkPort.commit()
            print(f"Data source {data_source.id} created")
        except Exception as e:
            UnitOfWorkPort.rollback()
            raise e


@execute_command.register(CreateDataSource)
def execute_create_data_source(command: CreateDataSource):
    handler = CreateDataSourceCommandHandler()
    handler.handle(command)
