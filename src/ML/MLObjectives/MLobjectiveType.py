from abc import ABC, abstractmethod
from models.bars import Bars
from tradeTypes.tradeType import TradeType
from indicators.indicatorType import IndicatorType


class MLObjectiveType(ABC):
    """ML Objectives provide objective functions to for optimization of TradeTypes and
    Indicators
    """

    @abstractmethod
    def __init__(
        self,
        trade_type: TradeType,
        indicator: IndicatorType,
        bars: Bars,
    ):
        pass

    @abstractmethod
    def objective(self):
        pass
