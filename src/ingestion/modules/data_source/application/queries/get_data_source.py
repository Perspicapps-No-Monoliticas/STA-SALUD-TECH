from seedwork.application.queries import DetailQuery, execute_query, QueryResult
from modules.data_source.domain.repositories import DataSourceRepository
from .base import DataSourceQueryBaseHandler
from modules.data_source.application.mappers import DataSourceMapper


class GetDataSource(DetailQuery): ...


class GetDataSourcesQueryHandler(DataSourceQueryBaseHandler):
    def handle(self, query: DetailQuery) -> QueryResult:
        repository = self.repository_factory.create_object(
            DataSourceRepository.__class__
        )
        data_sources = self.data_source_factory.create_object(
            repository.get_by_id(query.id), DataSourceMapper()
        )
        return QueryResult(result=data_sources)


@execute_query.register(DetailQuery)
def execute_get_all_data_sources(query: DetailQuery):
    handler = GetDataSourcesQueryHandler()
    return handler.handle(query)
