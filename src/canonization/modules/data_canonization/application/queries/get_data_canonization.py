from seedwork.application.queries import DetailQuery, execute_query, QueryResult
from modules.data_canonization.domain.repositories import DataCanonizationRepository
from .base import DataCanonizationeQueryBaseHandler
from modules.data_canonization.application.mappers import DataCanonizationMapper


class GetDataCanonization(DetailQuery): ...


class GetDataCanonizationsQueryHandler(DataCanonizationeQueryBaseHandler):
    def handle(self, query: GetDataCanonization) -> QueryResult:
        repository = self.repository_factory.create_object(
            DataCanonizationRepository.__class__
        )
        data_canonizations = self.data_canonization_factory.create_object(
            repository.get_by_id(query.id), DataCanonizationMapper()
        )
        return QueryResult(result=data_canonizations)


@execute_query.register(GetDataCanonization)
def execute_get_all_data_canonizations(query: GetDataCanonization):
    handler = GetDataCanonizationsQueryHandler()
    return handler.handle(query)
