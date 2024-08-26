

from abc import ABC, abstractmethod
from typing import Any, Dict


class Rule(ABC):
    @abstractmethod
    def apply(self, context: Dict[str, Any]) -> None:
        pass
