from abc import ABC, abstractmethod
from typing import Any, Dict, List
from auth.const import Actions
 
class IndicatorType(ABC):

  @abstractmethod
  def run(self, candles: List[Dict[Any, Any]]) -> Actions:
    pass