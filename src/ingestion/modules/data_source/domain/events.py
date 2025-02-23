from dataclasses import dataclass
import uuid
from datetime import datetime

from seedwork.domain.events import DomainEvent


@dataclass
class DataSourceCreated(DomainEvent):
    provider_id: uuid.UUID
    data_source_id: uuid.UUID
    created_at: datetime


@dataclass
class DataSourceUpdated(DomainEvent):
    provider_id: uuid.UUID
    data_source_id: uuid.UUID
    updated_at: datetime


@dataclass
class DataSourceDeleted(DomainEvent):
    provider_id: uuid.UUID
    data_source_id: uuid.UUID
    deleted_at: datetime
