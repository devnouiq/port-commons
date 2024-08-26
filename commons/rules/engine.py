from abc import ABC, abstractmethod
from typing import Dict, Any


class BusinessRule(ABC):
    @abstractmethod
    def apply(self, context: Dict[str, Any]) -> None:
        pass


class BusinessRuleEngine:
    def __init__(self, rules: list[BusinessRule]):
        self.rules = rules

    def apply_rules(self, context: Dict[str, Any]) -> None:
        for rule in self.rules:
            rule.apply(context)
