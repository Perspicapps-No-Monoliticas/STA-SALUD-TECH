import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict


class DataCanonizationStepSchema(BaseModel):
    id: uuid.UUID
    status: str
    created_at: datetime
    updated_at: datetime
    ai_model_id: uuid.UUID
    total_records: int
    model_config = ConfigDict(from_attributes=True)


class DataCanonizationDetailSchema(BaseModel):
    id: uuid.UUID
    provider_id: uuid.UUID
    anonimization_id: uuid.UUID
    ingestion_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    status: str
    total_records: int
    repository_in_path: str
    steps: List[DataCanonizationStepSchema]
    model_config = ConfigDict(from_attributes=True)


class IntakeInitSchema(BaseModel):
    provider_id: uuid.UUID
    anonimization_id: uuid.UUID
    ingestion_id: uuid.UUID
    repository_in_path: str
