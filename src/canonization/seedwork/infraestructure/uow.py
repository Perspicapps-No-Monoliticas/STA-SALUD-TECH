from abc import ABC, abstractmethod
from enum import Enum
from threading import local

from seedwork.domain.entities import RootAgregation
from pydispatch import dispatcher


class Lock(Enum):
    OPTIMIST = 1
    PESIMITS = 2


class Batch:
    def __init__(self, operation, lock: Lock, *args, **kwargs):
        self.operation = operation
        self.args = args
        self.lock = lock
        self.kwargs = kwargs


class UnitOfWork(ABC):

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    def _get_events(self, batches=None):
        batches = self.batches if batches is None else batches
        for batch in batches:
            for arg in batch.args:
                if isinstance(arg, RootAgregation):
                    return arg.events
        return list()

    @abstractmethod
    def _clean_batches(self):
        raise NotImplementedError

    @abstractmethod
    def batches(self) -> list[Batch]:
        raise NotImplementedError

    @abstractmethod
    def savepoints(self) -> list:
        raise NotImplementedError

    def commit(self):
        self._publish_events_post_commit()
        self._clean_batches()

    @abstractmethod
    def rollback(self, savepoint=None):
        self._clean_batches()

    @abstractmethod
    def savepoint(self):
        raise NotImplementedError

    def register_batch(self, operation, *args, lock=Lock.PESIMITS, **kwargs):
        batch = Batch(operation, lock, *args, **kwargs)
        self.batches.append(batch)
        self._publish_domain_events(batch)

    def _publish_domain_events(self, batch):
        for event in self._get_events(batches=[batch]):
            dispatcher.send(signal=f"{type(event).__name__}Domain", event=event)

    def _publish_events_post_commit(self):
        for event in self._get_events():
            dispatcher.send(signal=f"{type(event).__name__}Integration", event=event)


_thread_local = local()


def sql_alcehmy_unit_of_work():
    from config.uow import UnitOfWorkSQLAlchmey

    return UnitOfWorkSQLAlchmey()


def unit_of_work() -> UnitOfWork:
    uow = getattr(_thread_local, "uow", None)
    if not uow:
        uow = sql_alcehmy_unit_of_work()
        setattr(_thread_local, "uow", uow)
    return uow


def save_unit_of_work(uow: UnitOfWork):
    setattr(_thread_local, "uow", uow)


class UnitOfWorkPort:

    @staticmethod
    def commit():
        uow = unit_of_work()
        uow.commit()
        save_unit_of_work(uow)

    @staticmethod
    def rollback(savepoint=None):
        uow = unit_of_work()
        uow.rollback(savepoint=None)
        save_unit_of_work(uow)

    @staticmethod
    def savepoint():
        uow = unit_of_work()
        uow.savepoint()
        save_unit_of_work(uow)

    @staticmethod
    def get_savepoints():
        uow = unit_of_work()
        return uow.savepoints()

    @staticmethod
    def register_batch(operation, *args, lock=Lock.PESIMITS, **kwargs):
        uow = unit_of_work()
        uow.register_batch(operation, *args, lock=lock, **kwargs)
        save_unit_of_work(uow)
