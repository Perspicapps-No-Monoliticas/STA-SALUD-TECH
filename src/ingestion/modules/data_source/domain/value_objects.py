from enum import Enum
from dataclasses import dataclass

from seedwork.domain.value_objects import ValueObject


class DataSourceType(str, Enum):
    POSTGRES = "POSTGRES"
    MySQL = "MySQL"
    API = "API"
    DROPBOX = "DROPBOX"
    AWS_S3 = "AWS_S3"


class CredentialType(str, Enum):
    PASSWORD = "PASSWORD"
    TOKEN = "TOKEN"
    CERTIFICATE = "CERTIFICATE"


@dataclass(frozen=True)
class Credentials(ValueObject):
    payload: dict
    type: CredentialType


@dataclass(frozen=True)
class Information(ValueObject):
    name: str
    description: str
