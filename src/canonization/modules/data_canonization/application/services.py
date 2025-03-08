import uuid
import time
import random

from modules.data_canonization.domain.entities import DataCanonization
from modules.data_canonization.domain.services import (
    ProcessCanonizationService as DomainProcessCanonizationService,
)
from modules.data_canonization.domain.factories import DataCanonizationFactory
from modules.data_canonization.infrastructure.factories import RepositoryFactory
from modules.data_canonization.domain.repositories import (
    DataCanonizationRepository,
    DataCanonizationStepRepository,
)
from .mappers import DataCanonizationMapper


from seedwork.infrastructure.uow import UnitOfWorkPort
from seedwork.infrastructure.varaibles import (
    PROCESSING_TIME_WAIT_MIN,
    PROCESSING_TIME_WAIT_MAX,
)


def _save_uow():
    try:
        UnitOfWorkPort.savepoint()
        UnitOfWorkPort.commit()
    except Exception as e:
        UnitOfWorkPort.rollback()
        raise e
    #  Wait some time


class ProcessCanonizationService(DomainProcessCanonizationService):

    def __init__(self):
        self.data_canonization_repository: DataCanonizationRepository = (
            RepositoryFactory().create_object(DataCanonizationRepository.__class__)
        )
        self.data_canonization_step_repository: DataCanonizationStepRepository = (
            RepositoryFactory().create_object(DataCanonizationStepRepository.__class__)
        )
        self.data_canonization_factory: DataCanonizationFactory = (
            DataCanonizationFactory()
        )
        self.data_canonization_mapper: DataCanonizationMapper = DataCanonizationMapper()
        super().__init__()

    def process_canonization(
        self, canonization_uuid: uuid.UUID, correlation_uuid: uuid.UUID
    ):
        # Connect evetns

        from modules.data_canonization.application.handle_domain_events import (
            init_producers,
        )

        init_producers()
        print(f"Processing canonization {canonization_uuid}")
        #  Change status of canonization
        data_canonization: DataCanonization = (
            self.data_canonization_repository.get_by_id(canonization_uuid)
        )
        data_canonization.start_canonization(correlation_uuid)
        UnitOfWorkPort.register_batch(
            self.data_canonization_repository.update, data_canonization
        )
        _save_uow()
        data_canonization: DataCanonization = (
            self.data_canonization_repository.get_by_id(canonization_uuid)
        )
        print(f"Data canonization {data_canonization.id} started")
        time.sleep(random.randint(PROCESSING_TIME_WAIT_MIN, PROCESSING_TIME_WAIT_MAX))
        data_canonization.finish_canonization(correlation_uuid)
        UnitOfWorkPort.register_batch(
            self.data_canonization_repository.update, data_canonization
        )
        print(f"Data canonization {data_canonization.id} ended")
        _save_uow()
