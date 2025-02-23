from functools import cached_property
import uuid

from config.db import db

from modules.data_source.domain.repositories import DataSourceRepository
from modules.data_source.domain.factories import DataSourceFactory
from modules.data_source.domain import entities as domain_entities
from .dto import DataSource as DataSourceDTO
from .mappers import DataSourceMapper


class DataSurceSQLAlchemyRepository(DataSourceRepository):

    def __init__(self):
        self._data_source_factory: DataSourceFactory = DataSourceFactory()

    @property
    def data_source_factory(self) -> DataSourceFactory:
        return self._data_source_factory

    def get_by_id(self, data_source_id: uuid.UUID) -> domain_entities.DataSource:
        data_source_dto = (
            db.query(DataSourceDTO).filter(DataSourceDTO.id == data_source_id).first()
        )

    def add(self, data_source: domain_entities.DataSource):
        data_source_dto: DataSourceDTO = self.data_source_factory.create_object(
            data_source, DataSourceMapper()
        )
        db.add(data_source_dto)

    def update(self, data_source: domain_entities.DataSource):
        db.add(data_source)

    def delete(self, data_source: domain_entities.DataSource):
        db.delete(data_source)

    def get_all(self):
        return db.query(DataSourceDTO).all()
