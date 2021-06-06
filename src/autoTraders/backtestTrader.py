from typing import Iterable
from alpaca_trade_api.rest import TimeFrame
from tradeTypes.tradeType import TradeType
from models.bars import Bars
from indicators.indicatorType import IndicatorType
from datetime import datetime, timedelta
from dataAPIs.dataAPIType import DataAPIType


class BacktestTrader:
    def __init__(
        self,
        trade_type: TradeType,
        indicator: IndicatorType,
        data_api: DataAPIType,
        start: datetime = datetime.now() - timedelta(days=7),
        end: datetime = datetime.now(),
    ):
        self.bars = []
        self.tradeType = trade_type
        self.indicator = indicator
        self.data_api = data_api
        self.start = start
        self.end = end

    @staticmethod
    def start_traders(traders: Iterable["BacktestTrader"]):
        for t in traders:
            t.bars = t.data_api.get_bars_timeframe(
                t.tradeType.symbol, TimeFrame.Minute, t.start, t.end
            ).get_bars()

            for index, bar in t.bars.iterrows():
                # Get indicator result from data and pass to tradeType to execute
                decision = t.indicator.run(Bars(t.bars[:index]))
                t.tradeType.handle(decision, bar)
