from abc import ABC, abstractmethod
from typing import Any, Dict, List
from auth.const import Actions


class IndicatorType(ABC):
    @abstractmethod
    def run(self, candle: Dict[Any, Any]) -> Actions:
        pass
