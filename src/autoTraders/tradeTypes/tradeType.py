from abc import ABC, abstractmethod
from typing import Any, Dict
from auth.const import Actions
 
class TradeType(ABC):

  @abstractmethod
  def handle(self, res: Actions, currentCandle: Dict[Any, Any]) -> None:
    pass

  @property
  @abstractmethod
  def symbol(self) -> str:
    pass