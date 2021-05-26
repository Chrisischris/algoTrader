from abc import ABC, abstractmethod
from auth.const import Actions
from models.bars import Bars


class TradeType(ABC):
    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def handle(self, res: Actions, currentCandle: Bars) -> None:
        pass

    @property
    @abstractmethod
    def symbol(self) -> str:
        pass
