from typing import List
from dataclasses import dataclass, field
import uuid

from seedwork.domain.entities import RootAgregation, Entity
from .value_objects import DataIntakeStatus, IntakeSpecs
from .events import DataintakeStarted


@dataclass
class IntakeStep(Entity):
    data_source_id: uuid.UUID = field(default=None)
    total_records: int = field(default=None)
    status: DataIntakeStatus = field(default=None)


@dataclass
class DataIntake(RootAgregation):
    provider_id: uuid.UUID = field(default=None)
    status: DataIntakeStatus = field(default=None)
    specs: IntakeSpecs = field(default=None)
    history: List[IntakeStep] = field(default=None)

    def create_data_intake(self, data_intake: "DataIntake"):
        self.provider_id = data_intake.provider_id
        self.status = data_intake.status
        self.specs = data_intake.specs
        self.history = data_intake.history

        self.add_event(
            DataintakeStarted(
                provider_id=self.provider_id,
                data_intake_id=self.id,
                created_at=self.created_at,
            )
        )
