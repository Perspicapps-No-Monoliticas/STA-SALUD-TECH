from enum import Enum
from datetime import datetime
import uuid

from modules.data_source.domain.value_objects import CredentialType, DataSourceType

from pydantic import BaseModel, Field, ConfigDict


class CredentialSchema(BaseModel):
    payload: dict
    type: CredentialType


class DataSourceCreationSchema(BaseModel):
    name: str = Field(max_length=255)
    description: str
    type: DataSourceType
    credentials: CredentialSchema
    model_config = ConfigDict(from_attributes=True)
    provider_id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)


class DataSourceDetailSchema(DataSourceCreationSchema):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
