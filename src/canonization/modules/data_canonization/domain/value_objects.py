from enum import Enum
from dataclasses import dataclass

from seedwork.domain.value_objects import ValueObject


class DataCanonizationStatus(str, Enum):
    CREATED = "CREATED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass(frozen=True)
class IntakeSpecs(ValueObject):
    total_records: int
    repository_in_path: str
