from enum import Enum
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class DataSourceType(Enum):
    SQL = "SQL"
    NoSQL = "NoSQL"
    API = "API"
    FILE = "FILE"


class CrentialType(Enum):
    PASSWORD = "PASSWORD"
    TOKEN = "TOKEN"
    CERTIFICATE = "CERTIFICATE"


class CredentialSchema(BaseModel):
    payload: dict
    source: CrentialType


class DataSourceCreationSchema(BaseModel):
    name: str = Field(max_length=255)
    description: str
    type: DataSourceType
    credentials: CredentialSchema
    model_config = ConfigDict(from_attributes=True)
    provider_id: int


class DataSourceDetailSchema(DataSourceCreationSchema):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
