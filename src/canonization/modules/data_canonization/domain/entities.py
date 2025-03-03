from typing import List
from dataclasses import dataclass, field
import uuid
from datetime import datetime

from seedwork.domain.entities import RootAgregation, Entity
from .value_objects import DataCanonizationStatus, CanonizationSpecs
from .events import (
    DataCanonizationCreated,
    DataCanonizationStarted,
    DataCanonizationFinished,
)


@dataclass
class CanonizationStep(Entity):
    data_canonization_id: uuid.UUID = field(default=None)
    ai_model_id: uuid.UUID = field(default=None)
    total_records: int = field(default=None)
    status: DataCanonizationStatus = field(default=None)


@dataclass
class DataCanonization(RootAgregation):
    provider_id: uuid.UUID = field(default=None)
    anonimization_id: str = field(default=None)
    ingestion_id: uuid.UUID = field(default=None)
    status: DataCanonizationStatus = field(default=None)
    specs: CanonizationSpecs = field(default=None)
    steps: List[CanonizationStep] = field(default=None)

    def create_data_canonization(self, correlation_id: uuid.UUID):
        self.status = DataCanonizationStatus.CREATED
        self.add_event(
            DataCanonizationCreated(
                data_canonization_id=self.id,
                correlation_id=correlation_id,
                created_at=datetime.now(),
            )
        )

    def start_canonization(self, correlation_id: uuid.UUID):
        self.status = DataCanonizationStatus.IN_PROGRESS
        self.add_event(
            DataCanonizationStarted(
                data_canonization_id=self.id,
                correlation_id=correlation_id,
                created_at=datetime.now(),
            )
        )

    def finish_canonization(self, correlation_id: uuid.UUID):
        self.status = DataCanonizationStatus.COMPLETED
        self.add_event(
            DataCanonizationFinished(
                data_canonization_id=self.id,
                correlation_id=correlation_id,
                created_at=datetime.now(),
            )
        )
