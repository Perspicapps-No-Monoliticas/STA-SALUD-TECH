from abc import ABC, abstractmethod
from enum import Enum

from seedwork.domain.entities import RootAgregation
from pydispatch import dispatcher

import pickle


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
                    return arg.eventos
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
        for evento in self._get_events(batches=[batch]):
            dispatcher.send(signal=f"{type(evento).__name__}Domain", evento=evento)

    def _publish_events_post_commit(self):
        for evento in self._get_events():
            dispatcher.send(signal=f"{type(evento).__name__}Integration", evento=evento)
