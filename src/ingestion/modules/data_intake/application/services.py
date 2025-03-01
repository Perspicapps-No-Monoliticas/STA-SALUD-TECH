import uuid
import time
import random

from modules.data_intake.domain.entities import DataIntake
from modules.data_intake.domain.services import (
    ProcessIngestionService as DomainProcessIngestionService,
)
from modules.data_intake.domain.factories import DataIntakeFactory
from modules.data_intake.infrastructure.factories import RepositoryFactory
from modules.data_intake.domain.repositories import (
    DataIntakeRepository,
    DataIntakeStepRepository,
)
from .mappers import DataIntakeMapper


from seedwork.infrastructure.uow import UnitOfWorkPort


def _save_uow():
    try:
        UnitOfWorkPort.savepoint()
        UnitOfWorkPort.commit()
    except Exception as e:
        UnitOfWorkPort.rollback()
        raise e
    #  Wait some time


class ProcessIngestionService(DomainProcessIngestionService):

    def __init__(self):
        self.data_intake_repository: DataIntakeRepository = (
            RepositoryFactory().create_object(DataIntakeRepository.__class__)
        )
        self.data_intake_step_repository: DataIntakeStepRepository = (
            RepositoryFactory().create_object(DataIntakeStepRepository.__class__)
        )
        self.data_intake_factory: DataIntakeFactory = DataIntakeFactory()
        self.data_intake_mapper: DataIntakeMapper = DataIntakeMapper()
        super().__init__()

    def process_ingestion(self, ingestion_uuid: uuid.UUID, correlation_id: uuid.UUID):
        # Connect evetns

        from modules.data_intake.application.handle_domain_events import init_producers

        init_producers()
        print(f"Processing ingestion {ingestion_uuid}")
        #  Change status of ingestion
        data_intake: DataIntake = self.data_intake_repository.get_by_id(ingestion_uuid)
        data_intake.start_ingestion(correlation_id)
        UnitOfWorkPort.register_batch(self.data_intake_repository.update, data_intake)
        _save_uow()
        data_intake: DataIntake = self.data_intake_repository.get_by_id(ingestion_uuid)
        print(f"Data ingestion {data_intake.id} started")
        time.sleep(random.randint(1, 10))
        data_intake.finish_ingestions(correlation_id)
        UnitOfWorkPort.register_batch(self.data_intake_repository.update, data_intake)
        print(f"Data ingestion {data_intake.id} ended")
        _save_uow()
