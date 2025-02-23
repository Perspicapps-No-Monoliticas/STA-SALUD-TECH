from functools import cached_property
from typing import Optional
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

    def get_by_id_raw(self, data_source_id: uuid.UUID) -> Optional[DataSourceDTO]:
        data_source_dto = (
            db.query(DataSourceDTO).filter(DataSourceDTO.id == data_source_id).first()
        )
        db.close()
        return data_source_dto

    def get_by_id(
        self, data_source_id: uuid.UUID
    ) -> Optional[domain_entities.DataSource]:
        data_source_dto = self.get_by_id_raw(data_source_id)

        return self.data_source_factory.create_object(
            data_source_dto, DataSourceMapper()
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

    def get_paginated(self, page: int, per_page: int):
        offset = (page - 1) * per_page
        dtos = db.query(DataSourceDTO).offset(offset).limit(per_page).all()
        db.close()
        return [
            self.data_source_factory.create_object(dto, DataSourceMapper())
            for dto in dtos
        ]
