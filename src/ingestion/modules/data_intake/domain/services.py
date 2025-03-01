from abc import ABC, abstractmethod
import uuid

from seedwork.domain.services import Service


class ProcessIngestionService(Service, ABC):
    @abstractmethod
    def process_ingestion(self, ingestion_uuid: uuid.UUID) -> None:
        pass
