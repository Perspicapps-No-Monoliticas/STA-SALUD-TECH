from typing import Dict, List

from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass(frozen=True)
class DTO: ...


class Mapper(ABC):
    @abstractmethod
    def external_to_dto(self, external: Dict | List) -> DTO: ...

    @abstractmethod
    def dto_to_external(self, dto: DTO) -> Dict | List: ...
