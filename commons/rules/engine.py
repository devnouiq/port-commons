from abc import ABC, abstractmethod
from typing import Dict, Any
from commons.utils.logger import get_logger

logger = get_logger()


class BusinessRule(ABC):
    @abstractmethod
    def apply(self, context: Dict[str, Any]) -> None:
        pass


class BusinessRuleEngine:
    def __init__(self, rules: list[BusinessRule]):
        self.rules = rules

    def apply_rules(self, context: Dict[str, Any]) -> None:
        logger.info("Applying rules...")
        for rule in self.rules:
            logger.info(f"Applying rule: {rule.__class__.__name__}")
            rule.apply(context)
