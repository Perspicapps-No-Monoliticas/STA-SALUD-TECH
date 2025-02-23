from dataclasses import dataclass, field
import uuid
from datetime import datetime
from typing import List

from seedwork.domain.rules import InmitableEntity
from seedwork.domain.exceptions import InmutableIdException
from seedwork.domain.mixins import RuleValidationMixin
from seedwork.domain.events import DomainEvent


@dataclass
class Entity:
    id: uuid.UUID = field(hash=True)
    _id: uuid.UUID = field(init=False, repr=False, hash=True)
    created_at: datetime = field(default=datetime.now())
    updated_at: datetime = field(default=datetime.now())

    @classmethod
    def next_id(cls) -> uuid.UUID:
        return uuid.uuid4()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, _id: uuid.UUID) -> None:
        if not InmitableEntity(self).is_valid():
            raise InmutableIdException()
        self._id = self.next_id()


@dataclass
class RootAgregation(Entity, RuleValidationMixin):
    events: List[DomainEvent] = field(default_factory=list)

    def add_event(self, event: DomainEvent):
        self.events.append(event)

    def clean_eventd(self):
        self.events = list()
