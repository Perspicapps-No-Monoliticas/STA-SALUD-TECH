from dataclasses import dataclass
import uuid
from datetime import datetime

from seedwork.domain.events import DomainEvent


@dataclass
class DataCanonizationCreated(DomainEvent):
    data_canonization_id: uuid.UUID
    created_at: datetime
    correlation_id: uuid.UUID


@dataclass
class DataCanonizationStarted(DataCanonizationCreated): ...


@dataclass
class DataCanonizationFinished(DataCanonizationCreated): ...


@dataclass
class DataCanonizationStepStarted(DomainEvent):
    data_canonization_step_id: uuid.UUID


@dataclass
class DataCanonizationStepFinished(DomainEvent):
    data_canonization_step_id: uuid.UUID
