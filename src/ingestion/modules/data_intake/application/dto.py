from dataclasses import dataclass, field
import uuid
from datetime import datetime


from seedwork.application.dto import DTO


@dataclass(frozen=True)
class DataIntakeStepDTO(DTO):
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    status: str = field(default_factory=str)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    data_source_id: uuid.UUID = field(default_factory=uuid.uuid4)
    total_records: int = field(default_factory=int)


@dataclass(frozen=True)
class DataIntakeDTO(DTO):
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    provider_id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    status: str = field(default_factory=str)
    total_records: int = field(default_factory=int)
    repository_out_path: str = field(default_factory=str)
    history: DataIntakeStepDTO = field(default_factory=list)
