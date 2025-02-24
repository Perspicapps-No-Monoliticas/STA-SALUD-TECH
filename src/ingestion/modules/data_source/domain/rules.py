from seedwork.domain.rules import BussinessRule
from .value_objects import Credentials, DataSourceType
from uuid import UUID


class HasCredentials(BussinessRule):

    credentials: Credentials

    def __init__(self, credentials: Credentials, message: str = "None"):
        super().__init__(message)
        self.credentials = credentials

    def is_valid(self) -> bool:
        if not self.credentials.payload:
            return False
        return True


class ValidDataSourceType(BussinessRule):

    data_source_type: DataSourceType

    def __init__(
        self,
        data_source_type: DataSourceType,
        message: str = "Invalid data source type",
    ):
        super().__init__(message)
        self.data_source_type = data_source_type

    def is_valid(self) -> bool:
        return self.data_source_type in DataSourceType
