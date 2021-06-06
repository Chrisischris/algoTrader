from abc import ABC, abstractmethod
from auth.const import Actions
from models.bars import Bars
from typing import List


class IndicatorType(ABC):
    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def run(self, bars: Bars) -> Actions:
        """Returns a single action based on bars

        Args:
            bars (Bars): Price history

        Returns:
            Actions: The action determined
        """
        pass

    @abstractmethod
    def backtest(self, bars: Bars) -> List:
        """Backtest an indicator with this, it will return a list that contains an
            action for each bar

        Args:
            bars (Bars): Price History

        Returns:
            List: List of actions
        """
        pass
