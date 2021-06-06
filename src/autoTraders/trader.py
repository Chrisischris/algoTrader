from typing import Iterable
from tradeTypes.tradeType import TradeType
from indicators.indicatorType import IndicatorType
from dataAPIs.dataAPIType import DataAPIType


class Trader:
    def __init__(
        self,
        trade_type: TradeType,
        indicator: IndicatorType,
        data_api: DataAPIType,
    ):
        self.candles = []
        self.trade_type = trade_type
        self.indicator = indicator
        self.data_api = data_api

    @staticmethod
    def start_traders(traders: Iterable["Trader"]):
        symbols = []
        for t in traders:
            symbols.append(t.trade_type.symbol)

        if len(symbols):
            # TODO Start streaming data for the symbols
            pass
