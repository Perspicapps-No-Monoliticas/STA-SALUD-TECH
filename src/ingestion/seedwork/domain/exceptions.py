from .rules import BussinessRule


class DomainException(Exception): ...


class InmutableIdException(DomainException):
    def __init__(self, message: str = "Id should be inmutable"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class BussinesRuleException(DomainException):
    def __init__(self, rule: BussinessRule):
        self.rule = rule
        super().__init__(rule.error_message)

    def __str__(self):
        return self.rule.error_message


class FactoryException(DomainException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message
