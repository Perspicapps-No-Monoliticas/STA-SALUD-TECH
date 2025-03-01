from seedwork.application.queries import QueryHandler


from modules.data_canonization.domain.factories import DataCanonizationFactory
from modules.data_canonization.infraestrucuture.factories import RepositoryFactory


class DataCanonizationeQueryBaseHandler(QueryHandler):
    def __init__(self):
        self._repository_factory: RepositoryFactory = RepositoryFactory()
        self._data_canonization_factory: DataCanonizationFactory = DataCanonizationFactory()
        super().__init__()

    @property
    def repository_factory(self) -> RepositoryFactory:
        return self._repository_factory

    @property
    def data_canonization_factory(self) -> DataCanonizationFactory:
        return self._data_canonization_factory
