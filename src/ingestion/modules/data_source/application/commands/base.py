from seedwork.application.commands import CommandHandler

from modules.data_source.domain.factories import DataSourceFactory
from modules.data_source.infraestrucuture.factories import RepositoryFactory


class CreateDataSourceBaseHandler(CommandHandler):

    def __init__(self):
        self._repository_factory: RepositoryFactory = RepositoryFactory()
        self._data_source_factory: DataSourceFactory = DataSourceFactory()
        super().__init__()

    @property
    def repository_factory(self) -> RepositoryFactory:
        return self._repository_factory

    @property
    def data_source_factory(self) -> DataSourceFactory:
        return self._data_source_factory
