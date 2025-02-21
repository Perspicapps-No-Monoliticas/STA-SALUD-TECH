from dataclasses import dataclass
from modules.data_source.application.dto import CredentialsDTO, DataSourceDTO
from seedwork.application.commands import Command, execute_command


@dataclass
class CreateDataSource(Command):
    name: str
    description: str
    type: str
    credentials: CredentialsDTO
    provider_id: int

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


class CreateDataSourceCommandHandler:
    def handle(self, command: CreateDataSource):
        data_source_dto = command.to_dto()


@execute_command.register(CreateDataSource)
def execute_create_data_source(command: CreateDataSource):
    handler = CreateDataSourceCommandHandler()
    handler.handle(command)
