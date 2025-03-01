from abc import ABC

from seedwork.domain.repositories import Repository


class DataCanonizationRepository(Repository, ABC): ...


class DataCanonizationStepRepository(Repository, ABC): ...
