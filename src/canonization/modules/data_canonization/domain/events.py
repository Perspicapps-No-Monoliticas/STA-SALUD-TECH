from dataclasses import dataclass
import uuid

from seedwork.domain.events import DomainEvent


@dataclass
class DataCanonizationStarted(DomainEvent):
    data_canonization_id: uuid.UUID


@dataclass
class DataCanonizationFinished(DomainEvent):
    data_canonization_id: uuid.UUID


@dataclass
class DataCanonizationStepStarted(DomainEvent):
    data_canonization_step_id: uuid.UUID


@dataclass
class DataCanonizationStepFinished(DomainEvent):
    data_canonization_step_id: uuid.UUID
