from dataclasses import dataclass, field
from datetime import datetime
import uuid

from seedwork.application.dto import DTO


@dataclass(frozen=True)
class CredentialsDTO(DTO):
    payload: dict = field(default=dict)
    type: str = field(default_factory=str)


@dataclass(frozen=True)
class DataSourceDTO(DTO):
    id: int = field(default_factory=int)
    provider_id: uuid.UUID = field(default_factory=uuid.uuid4)
    name: str = field(default_factory=str)
    description: str = field(default_factory=str)
    type: str = field(default_factory=str)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    credentials: CredentialsDTO = field(default_factory=CredentialsDTO)
