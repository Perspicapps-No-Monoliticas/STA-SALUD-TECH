from seedwork.infrastructure.uow import UnitOfWork, Batch
from .db import db


class UnitOfWorkSQLAlchmey(UnitOfWork):

    def __init__(self):
        self._batches: list[Batch] = list()
        self.session = db

    def __enter__(self) -> UnitOfWork:
        return super().__enter__()

    def __exit__(self, *args):
        self.rollback()

    def _clean_batches(self):
        self._batches = list()

    @property
    def savepoints(self) -> list:
        return list[self.session.get_nested_transaction()]

    @property
    def batches(self) -> list[Batch]:
        return self._batches

    def commit(self):
        for batch in self.batches:
            lock = batch.lock
            batch.operation(*batch.args, **batch.kwargs)

        self.session.commit()
        super().commit()
        self.session.close()

    def rollback(self, savepoint=None):
        if savepoint:
            savepoint.rollback()
        else:
            self.session.rollback()

        super().rollback()

    def savepoint(self):
        self.session.begin_nested()
