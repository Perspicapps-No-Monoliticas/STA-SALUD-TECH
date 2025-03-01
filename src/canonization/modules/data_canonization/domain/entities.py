from typing import List
from dataclasses import dataclass, field
import uuid

from seedwork.domain.entities import RootAgregation, Entity
from .value_objects import DataCanonizationStatus, IntakeSpecs
from .events import DataCanonizationStarted


@dataclass
class IntakeStep(Entity):
    data_canonization_id: uuid.UUID = field(default=None)
    ai_model_id: uuid.UUID = field(default=None)
    total_records: int = field(default=None)
    status: DataCanonizationStatus = field(default=None)


@dataclass
class DataCanonization(RootAgregation):
    provider_id: uuid.UUID = field(default=None)
    anonimization_id: uuid.UUID = field(default=None)
    ingestion_id: uuid.UUID = field(default=None)
    status: DataCanonizationStatus = field(default=None)
    specs: IntakeSpecs = field(default=None)
    steps: List[IntakeStep] = field(default=None)

    def create_data_canonization(self, data_canonization: "DataCanonization"):
        self.provider_id = data_canonization.provider_id
        self.status = data_canonization.status
        self.specs = data_canonization.specs
        self.steps = data_canonization.steps

        self.add_event(
            DataCanonizationStarted(
                data_canonization_id=self.id,
            )
        )
