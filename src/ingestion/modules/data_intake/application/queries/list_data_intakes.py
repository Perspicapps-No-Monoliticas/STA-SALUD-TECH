from seedwork.application.queries import PaginationQuery, execute_query, QueryResult
from modules.data_intake.domain.repositories import DataIntakeRepository

from modules.data_intake.application.mappers import DataIntakeMapper
from .base import DataIntakeeQueryBaseHandler


class GetAllDataIntakesQuery(PaginationQuery): ...


class GetAllDataSourcesQueryHandler(DataIntakeeQueryBaseHandler):
    def handle(self, query: GetAllDataIntakesQuery) -> QueryResult:
        repository = self.repository_factory.create_object(
            DataIntakeRepository.__class__
        )
        data_sources = self.data_intake_factory.create_object(
            repository.get_paginated(query.page, query.limit), DataIntakeMapper()
        )
        return QueryResult(result=data_sources)


@execute_query.register(GetAllDataIntakesQuery)
def execute_get_all_data_sources(query: GetAllDataIntakesQuery):
    handler = GetAllDataSourcesQueryHandler()
    return handler.handle(query)
