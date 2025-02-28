from typing import Any, Optional
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import singledispatch
import uuid


class Query(ABC): ...


@dataclass
class PaginationQuery(Query):
    page: Optional[int] = None
    limit: Optional[int] = None

    def __post_init__(self):
        if self.page is None:
            self.page = 1
        if self.limit is None:
            self.limit = 10


@dataclass
class DetailQuery(Query):
    id: uuid.UUID


@dataclass
class QueryResult:
    result: Any = None


class QueryHandler(ABC):
    @abstractmethod
    def handle(self, query: Query) -> QueryResult:
        raise NotImplementedError()


@singledispatch
def execute_query(query) -> QueryResult:
    raise NotImplementedError(
        f"Query handler not found for query {query.__class__.__name__}"
    )
