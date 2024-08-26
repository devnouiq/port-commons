from fastapi import HTTPException
from typing import Any, Dict
from base import Rule


class BusinessRuleEngine:
    def __init__(self, rules: list[Rule]):
        self.rules = rules

    def apply_rules(self, context: Dict[str, Any]) -> None:
        for rule in self.rules:
            rule.apply(context)


def apply_business_rules(context: Dict[str, Any], rules: list[Rule]):
    rule_engine = BusinessRuleEngine(rules)
    try:
        rule_engine.apply_rules(context)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
