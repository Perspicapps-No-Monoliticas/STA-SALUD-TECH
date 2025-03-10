from seedwork.application.queries import QueryHandler


from modules.data_intake.domain.factories import DataIntakeFactory
from modules.data_intake.infrastructure.factories import RepositoryFactory


class DataIntakeeQueryBaseHandler(QueryHandler):
    def __init__(self):
        self._repository_factory: RepositoryFactory = RepositoryFactory()
        self._data_intake_factory: DataIntakeFactory = DataIntakeFactory()
        super().__init__()

    @property
    def repository_factory(self) -> RepositoryFactory:
        return self._repository_factory

    @property
    def data_intake_factory(self) -> DataIntakeFactory:
        return self._data_intake_factory
