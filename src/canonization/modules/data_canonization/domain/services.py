from abc import ABC, abstractmethod
import uuid

from seedwork.domain.services import Service


class ProcessCanonizationService(Service, ABC):
    @abstractmethod
    def process_canonization(
        self, canonization_uuid: uuid.UUID, correlation_uuid: uuid.UUID
    ) -> None:
        pass
