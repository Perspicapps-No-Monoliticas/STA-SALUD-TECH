from abc import ABC

from seedwork.domain.repositories import Repository


class DataIntakeRepository(Repository, ABC): ...


class DataIntakeStepRepository(Repository, ABC): ...
