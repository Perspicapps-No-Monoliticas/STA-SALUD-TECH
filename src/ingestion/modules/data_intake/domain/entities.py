from typing import List
from dataclasses import dataclass, field
import uuid
from datetime import datetime

from seedwork.domain.entities import RootAgregation, Entity
from .value_objects import DataIntakeStatus, IntakeSpecs
from .events import DataintakeCreated, DataIntakeStarted, DataIntakeFinished


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

    def create_data_intake(self, data_intake: "DataIntake", correlation_id: uuid.UUID):
        self.provider_id = data_intake.provider_id
        self.status = data_intake.status
        self.specs = data_intake.specs
        self.history = data_intake.history

        self.add_event(
            DataintakeCreated(
                data_intake_id=self.id,
                created_at=self.created_at,
                correlation_id=correlation_id,
            )
        )

    def start_ingestion(self, correlation_id: uuid.UUID):
        self.status = DataIntakeStatus.IN_PROGRESS
        self.updated_at = datetime.now()
        self.add_event(
            DataIntakeStarted(
                data_intake_id=self.id,
                created_at=self.created_at,
                correlation_id=correlation_id,
            )
        )

    def finish_ingestions(self, correlation_id: uuid.UUID):
        self.status = DataIntakeStatus.COMPLETED
        self.updated_at = datetime.now()
        self.add_event(
            DataIntakeFinished(
                data_intake_id=self.id,
                created_at=self.created_at,
                correlation_id=correlation_id,
            )
        )
