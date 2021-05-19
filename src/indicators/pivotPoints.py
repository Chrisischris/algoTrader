from alpaca_trade_api.rest import TimeFrame
from pandas.core.series import Series
from dataAPIs.dataAPIType import DataAPIType
from indicators.indicatorType import IndicatorType
from outputHelpers.CSVBuilder import CSVBuilder
from datetime import datetime, timedelta
from typing import Any
from auth.const import Actions
from models.bars import Bars


# FIXME Partially Ready for Live Trading
# Important Info: Waits for 1 candle before action
class PivotPoints(IndicatorType):
    def __init__(self, symbol: str, dataAPI: DataAPIType):
        self.symbol = symbol
        self.dataAPI = dataAPI
        self.lastCandle: Series = Series()
        self.HLC = {
            "high": None,
            "low": None,
            "close": None,
            "datetime": None,
        }
        self.CSVBuilder = CSVBuilder(
            ["Date", "Action", "Price", "S2", "S1", "P", "R1", "R2"],
            "PivotPoints " + symbol,
        )

    # Pivot Point based trade signals, return BUY, SELL
    # Always use stop loss, sell signal not guarenteed
    def run(self, bars: Bars):
        candle = bars.get_latest_bar()
        HLC = self.getHLC(candle.name)

        if not HLC["close"]:
            return Actions.NONE
        elif self.lastCandle.empty:
            self.lastCandle = candle
            return Actions.NONE

        P = (HLC["high"] + HLC["low"] + HLC["close"]) / 3
        R1 = (P * 2) - HLC["low"]
        R2 = P + (HLC["high"] - HLC["low"])
        S1 = (P * 2) - HLC["high"]
        S2 = P - (HLC["high"] - HLC["low"])

        # TODO figure out shorting
        Action = Actions.NONE
        if self.lastCandle["close"] <= R1 and candle["close"] > R1:
            Action = Actions.BUY
        elif candle["close"] >= R2:
            Action = Actions.SELL

        self.CSVBuilder.write(
            [
                candle.name.isoformat(" "),
                Action,
                candle["close"],
                "{0:.2f}".format(S2),
                "{0:.2f}".format(S1),
                "{0:.2f}".format(P),
                "{0:.2f}".format(R1),
                "{0:.2f}".format(R2),
            ]
        )

        self.lastCandle = candle
        return Action

    # Return H, L, C for previous trading day
    def getHLC(self, currentTime: datetime) -> Any:
        # Don't re-request unless its a new day
        if not self.HLC["datetime"] or (
            currentTime - self.HLC["datetime"]
        ) >= timedelta(days=1):
            day_bars = self.dataAPI.get_bars_timeframe(
                self.symbol, TimeFrame.Day, currentTime - timedelta(days=2), currentTime
            ).get_bars()

            # TODO Make sure we get the right candle, timestamp > 24 hours old
            current = day_bars.iloc[len(day_bars) - 1]

            self.HLC = {
                "high": current["high"],
                "low": current["low"],
                "close": current["close"],
                "datetime": current.name,
            }

        return self.HLC
