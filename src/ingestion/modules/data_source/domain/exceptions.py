from seedwork.domain.exceptions import FactoryException


class ObjectTypeDoesNotExistInDataSourceDomain(FactoryException):

    def __init__(
        self,
        message="No factory  was found in the data source domain for the object type.",
    ):
        super().__init__(message)
