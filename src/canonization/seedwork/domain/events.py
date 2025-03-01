from dataclasses import dataclass, field
import uuid
from datetime import datetime
from seedwork.domain.exceptions import InmutableIdException
from seedwork.domain.rules import InmitableEntity


class DomainEvent:
    id: uuid.UUID = field(hash=True)
    _id: uuid.UUID = field(init=False, repr=False, hash=True)
    event_date: datetime = field(default=datetime.now())

    @classmethod
    def next_id(cls) -> uuid.UUID:
        return uuid.uuid4()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id: uuid.UUID) -> None:
        if not InmitableEntity(self).is_valid():
            raise InmutableIdException()
        self._id = self.next_id
