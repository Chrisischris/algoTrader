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
    def __init__(self, symbol: str, data_api: DataAPIType):
        self.symbol = symbol
        self.data_api = data_api
        self.last_bar: Series = Series()
        self.hlc = {
            "high": None,
            "low": None,
            "close": None,
            "datetime": None,
        }
        self.csv_builder = CSVBuilder(
            ["Date", "Action", "Price", "S2", "S1", "P", "R1", "R2"],
            "PivotPoints " + symbol,
        )

    # Pivot Point based trade signals, return BUY, SELL
    # Always use stop loss, sell signal not guaranteed
    def run(self, bars: Bars):
        candle = bars.get_latest_bar()
        hlc = self.get_hlc(candle.name)

        if not hlc["close"]:
            return Actions.NONE
        elif self.last_bar.empty:
            self.last_bar = candle
            return Actions.NONE

        p = (hlc["high"] + hlc["low"] + hlc["close"]) / 3
        r1 = (p * 2) - hlc["low"]
        r2 = p + (hlc["high"] - hlc["low"])
        s1 = (p * 2) - hlc["high"]
        s2 = p - (hlc["high"] - hlc["low"])

        # TODO figure out shorting
        action = Actions.NONE
        if self.last_bar["close"] <= r1 and candle["close"] > r1:
            action = Actions.BUY
        elif candle["close"] >= r2:
            action = Actions.SELL

        self.csv_builder.write(
            [
                candle.name.isoformat(" "),
                action,
                candle["close"],
                "{0:.2f}".format(s2),
                "{0:.2f}".format(s1),
                "{0:.2f}".format(p),
                "{0:.2f}".format(r1),
                "{0:.2f}".format(r2),
            ]
        )

        self.last_bar = candle
        return action

    # Return H, L, C for previous trading day
    def get_hlc(self, current_time: datetime) -> Any:
        # Don't re-request unless its a new day
        if not self.hlc["datetime"] or (
            current_time - self.hlc["datetime"]
        ) >= timedelta(days=1):
            day_bars = self.data_api.get_bars_timeframe(
                self.symbol,
                TimeFrame.Day,
                current_time - timedelta(days=2),
                current_time,
            ).get_bars()

            # TODO Make sure we get the right candle, timestamp > 24 hours old
            current = day_bars.iloc[len(day_bars) - 1]

            self.hlc = {
                "high": current["high"],
                "low": current["low"],
                "close": current["close"],
                "datetime": current.name,
            }

        return self.hlc
