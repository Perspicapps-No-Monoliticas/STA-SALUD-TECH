from typing import Optional, Generic, TypeVar, List
from config.db import Base, db
import uuid

from seedwork.domain.repositories import Repository
from seedwork.domain.factories import Factory
from seedwork.domain.repositories import Mapper


EnttyDTOType = TypeVar("EnttyDTOType")
EntityType = TypeVar("EntityType")


class SQLAlchemyRepository(Repository, Generic[EnttyDTOType, EntityType]):

    def __init__(
        self, entity_factory: Factory, entity_mapper: Mapper, alchemy_model: "Base"
    ):
        self.entity_factory = entity_factory()
        self.entity_mapper = entity_mapper()
        self.alchemy_model = alchemy_model
        super().__init__()

    def get_by_id_raw(self, enity_id: uuid.UUID) -> Optional[EnttyDTOType]:
        enity_dto = (
            db.query(self.alchemy_model)
            .filter(self.alchemy_model.id == enity_id)
            .first()
        )
        db.close()
        return enity_dto

    def get_by_id(self, enity_id: uuid.UUID) -> Optional[EntityType]:
        enity_dto = self.get_by_id_raw(enity_id)

        return self.entity_factory.create_object(enity_dto, self.entity_mapper)

    def add(self, data_source: EntityType):
        enity_dto: EnttyDTOType = self.entity_factory.create_object(
            data_source, self.entity_mapper
        )
        db.add(enity_dto)

    def update(self, data_source: EntityType):
        db.add(data_source)

    def delete(self, data_source: EntityType):
        db.delete(data_source)

    def get_all(self):
        return db.query(self.alchemy_model).all()

    def get_paginated(self, page: int, per_page: int) -> List[EntityType]:
        offset = (page - 1) * per_page
        dtos = db.query(self.alchemy_model).offset(offset).limit(per_page).all()
        result = [
            self.entity_factory.create_object(dto, self.entity_mapper) for dto in dtos
        ]
        db.close()

        return result
