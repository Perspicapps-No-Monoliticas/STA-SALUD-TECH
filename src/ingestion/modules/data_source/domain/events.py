from dataclasses import dataclass
import uuid
from datetime import datetime

from seedwork.domain.events import DomainEvent


@dataclass
class DataSourceCreated(DomainEvent):
    provider_id: uuid.UUID
    data_source_id: uuid.UUID
    created_at: datetime
