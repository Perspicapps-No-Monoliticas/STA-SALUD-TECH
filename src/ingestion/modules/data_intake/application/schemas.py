import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict


class DataIntakeStepSchema(BaseModel):
    id: uuid.UUID
    status: str
    created_at: datetime
    updated_at: datetime
    data_source_id: uuid.UUID
    total_records: int
    model_config = ConfigDict(from_attributes=True)


class DataIntakeDetailSchema(BaseModel):
    id: uuid.UUID
    provider_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    status: str
    total_records: int
    repository_out_path: str
    history: List[DataIntakeStepSchema]
    model_config = ConfigDict(from_attributes=True)


class IntakeInitSchema(BaseModel):
    provider_id: uuid.UUID
    coreography_id: uuid.UUID
