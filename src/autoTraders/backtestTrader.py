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
        tradeType: TradeType,
        indicator: IndicatorType,
        dataAPI: DataAPIType,
        start: datetime = datetime.now() - timedelta(days=7),
        end: datetime = datetime.now(),
    ):
        self.candles = []
        self.tradeType = tradeType
        self.indicator = indicator
        self.dataAPI = dataAPI
        self.start = start
        self.end = end

    @staticmethod
    def start_traders(traders: Iterable["BacktestTrader"]):
        for t in traders:
            t.candles = t.dataAPI.get_bars_timeframe(
                t.tradeType.symbol, TimeFrame.Minute, t.start, t.end
            ).get_bars()

            for index, candle in t.candles.iterrows():
                # Get indicator result from data and pass to tradeType to execute
                decision = t.indicator.run(Bars(t.candles[:index]))
                currentCandle = candle
                t.tradeType.handle(decision, currentCandle)
