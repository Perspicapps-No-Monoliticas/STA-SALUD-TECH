from modules.data_source.domain.repositories import DataSourceRepository
from modules.data_source.domain.factories import DataSourceFactory
from modules.data_source.domain import entities as domain_entities
from seedwork.infraestructure.repositories import SQLAlchemyRepository
from .dto import DataSource as DataSourceDTO
from .mappers import DataSourceMapper


class DataSourceSQLAlchemyRepository(
    DataSourceRepository,
    SQLAlchemyRepository[DataSourceDTO, domain_entities.DataSource],
):
    def __init__(self):
        super().__init__(DataSourceFactory, DataSourceMapper, DataSourceDTO)
