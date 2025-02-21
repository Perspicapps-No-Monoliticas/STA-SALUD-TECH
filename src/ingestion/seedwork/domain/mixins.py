from .rules import BussinessRule
from .exceptions import BussinesRuleException


class RuleValidationMixin:
    def validate_rule(self, rule: BussinessRule):
        if not rule.is_valid():
            raise BussinesRuleException(rule)
