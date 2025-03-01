from dataclasses import dataclass
import uuid
from datetime import datetime

from seedwork.domain.events import DomainEvent


@dataclass
class DataintakeCreated(DomainEvent):
    data_intake_id: uuid.UUID
    created_at: datetime
    coreography_id: uuid.UUID


@dataclass
class DataIntakeStepStarted(DomainEvent):
    data_intake_id: uuid.UUID
    provider_id: uuid.UUID
    data_intake_id_step_id: uuid.UUID
    created_at: datetime


@dataclass
class DataIntakeStarted(DataintakeCreated): ...


@dataclass
class DataIntakeFinished(DataIntakeStarted): ...
