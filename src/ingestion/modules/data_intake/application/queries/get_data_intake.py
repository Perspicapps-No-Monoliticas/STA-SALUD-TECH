from seedwork.application.queries import DetailQuery, execute_query, QueryResult
from modules.data_intake.domain.repositories import DataIntakeRepository
from .base import DataIntakeeQueryBaseHandler
from modules.data_intake.application.mappers import DataIntakeMapper


class GetDataIntake(DetailQuery): ...


class GetDataIntakesQueryHandler(DataIntakeeQueryBaseHandler):
    def handle(self, query: GetDataIntake) -> QueryResult:
        repository = self.repository_factory.create_object(
            DataIntakeRepository.__class__
        )
        data_intakes = self.data_intake_factory.create_object(
            repository.get_by_id(query.id), DataIntakeMapper()
        )
        return QueryResult(result=data_intakes)


@execute_query.register(GetDataIntake)
def execute_get_all_data_intakes(query: GetDataIntake):
    handler = GetDataIntakesQueryHandler()
    return handler.handle(query)
