from seedwork.application.queries import PaginationQuery, execute_query, QueryResult
from modules.data_source.domain.repositories import DataSourceRepository
from .base import DataSourceQueryBaseHandler
from modules.data_source.application.mappers import DataSourceMapper


class GetAllDataSourcesQuery(PaginationQuery): ...


class GetAllDataSourcesQueryHandler(DataSourceQueryBaseHandler):
    def handle(self, query: GetAllDataSourcesQuery) -> QueryResult:
        repository = self.repository_factory.create_object(
            DataSourceRepository.__class__
        )
        data_sources = self.data_source_factory.create_object(
            repository.get_paginated(query.page, query.limit), DataSourceMapper()
        )
        return QueryResult(result=data_sources)


@execute_query.register(GetAllDataSourcesQuery)
def execute_get_all_data_sources(query: GetAllDataSourcesQuery):
    handler = GetAllDataSourcesQueryHandler()
    return handler.handle(query)
