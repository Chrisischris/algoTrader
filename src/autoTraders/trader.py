from typing import Iterable
from tradeTypes.tradeType import TradeType
from indicators.indicatorType import IndicatorType
from dataAPIs.dataAPIType import DataAPIType


class Trader:
    def __init__(
        self,
        tradeType: TradeType,
        indicator: IndicatorType,
        dataAPI: DataAPIType,
    ):
        self.candles = []
        self.tradeType = tradeType
        self.indicator = indicator
        self.dataAPI = dataAPI

    @staticmethod
    def start_traders(traders: Iterable["Trader"]):
        symbols = []
        for t in traders:
            symbols.append(t.tradeType.symbol)

        if len(symbols):
            # TODO Start streaming data for the symbols
            pass
