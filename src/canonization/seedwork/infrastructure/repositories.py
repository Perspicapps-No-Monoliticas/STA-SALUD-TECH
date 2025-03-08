from typing import Optional, Generic, TypeVar, List, Callable
from config.db import Base, db
import uuid

from sqlalchemy.orm import Query

from seedwork.domain.repositories import Repository
from seedwork.domain.factories import Factory
from seedwork.domain.repositories import Mapper


EntityDTOType = TypeVar("EnttyDTOType")
EntityType = TypeVar("EntityType")


class SQLAlchemyRepository(Repository, Generic[EntityDTOType, EntityType]):

    def __init__(
        self, entity_factory: Factory, entity_mapper: Mapper, alchemy_model: "Base"
    ):
        self.entity_factory = entity_factory()
        self.entity_mapper = entity_mapper()
        self.alchemy_model = alchemy_model
        super().__init__()

    def get_by_id_raw(self, enity_id: uuid.UUID) -> Optional[EntityDTOType]:
        enity_dto = (
            db.query(self.alchemy_model)
            .filter(self.alchemy_model.id == enity_id)
            .first()
        )
        return enity_dto

    def get_by_id(self, enity_id: uuid.UUID) -> Optional[EntityType]:
        enity_dto = self.get_by_id_raw(enity_id)

        return self.entity_factory.create_object(enity_dto, self.entity_mapper)

    def add(self, data_source: EntityType):
        enity_dto: EntityDTOType = self.entity_factory.create_object(
            data_source, self.entity_mapper
        )
        db.add(enity_dto)

    def update(self, data_source: EntityType):
        entity_dto = self.entity_factory.create_object(data_source, self.entity_mapper)
        db.merge(entity_dto)

    def delete(self, data_source: EntityType):
        entity_dto = self.entity_factory.create_object(data_source, self.entity_mapper)
        db.delete(entity_dto)

    def get_all(self):
        query = db.query(self.alchemy_model).all()
        result = [
            self.entity_factory.create_object(dto, self.entity_mapper) for dto in query
        ]
        return result

    def get_paginated(
        self,
        page: int,
        per_page: int,
        extra_q: Optional[Callable[[Query], Query]] = None,
    ) -> List[EntityType]:
        offset = (page - 1) * per_page
        query = db.query(self.alchemy_model)
        if extra_q:
            query = extra_q(query)
        dtos = (
            query.order_by(self.alchemy_model.created_at.desc())
            .offset(offset)
            .limit(per_page)
            .all()
        )
        result = [
            self.entity_factory.create_object(dto, self.entity_mapper) for dto in dtos
        ]
        return result
