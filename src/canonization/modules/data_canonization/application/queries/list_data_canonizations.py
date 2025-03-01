from seedwork.application.queries import PaginationQuery, execute_query, QueryResult
from modules.data_canonization.domain.repositories import DataCanonizationRepository

from modules.data_canonization.application.mappers import DataCanonizationMapper
from .base import DataCanonizationeQueryBaseHandler


class GetAllDataCanonizationsQuery(PaginationQuery): ...


class GetAllDataCanonizationsQueryHandler(DataCanonizationeQueryBaseHandler):
    def handle(self, query: GetAllDataCanonizationsQuery) -> QueryResult:
        repository = self.repository_factory.create_object(
            DataCanonizationRepository.__class__
        )
        data_canonizations = self.data_canonization_factory.create_object(
            repository.get_paginated(query.page, query.limit), DataCanonizationMapper()
        )
        return QueryResult(result=data_canonizations)


@execute_query.register(GetAllDataCanonizationsQuery)
def execute_get_all_data_canonizations(query: GetAllDataCanonizationsQuery):
    handler = GetAllDataCanonizationsQueryHandler()
    return handler.handle(query)
