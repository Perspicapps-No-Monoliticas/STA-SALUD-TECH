from dataclasses import dataclass, field
import uuid
from datetime import datetime


from seedwork.application.dto import DTO


@dataclass(frozen=True)
class DataCanonizationStepDTO(DTO):
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    ai_model_id: uuid.UUID = field(default_factory=uuid.uuid4)
    status: str = field(default_factory=str)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    data_canonization_id: uuid.UUID = field(default_factory=uuid.uuid4)
    total_records: int = field(default_factory=int)


@dataclass(frozen=True)
class DataCanonizationDTO(DTO):
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    provider_id: uuid.UUID = field(default_factory=uuid.uuid4)
    ingestion_id: uuid.UUID = field(default_factory=uuid.uuid4)
    anonimization_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    status: str = field(default_factory=str)
    total_records: int = field(default_factory=int)
    repository_in_path: str = field(default_factory=str)
    steps: DataCanonizationStepDTO = field(default_factory=list)
    correlation_id: uuid.UUID = field(default_factory=uuid.uuid4)
