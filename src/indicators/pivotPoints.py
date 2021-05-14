from indicators.indicatorType import IndicatorType
from outputHelpers.CSVBuilder import CSVBuilder
from data_apis.request import getClient, request
from datetime import datetime, timedelta
from typing import Any, Dict, List
from auth.const import Actions
from tda import client
import sys
import json

# FIXME Partially Ready for Live Trading
# Important Info: Waits for 1 candle before action
class PivotPoints(IndicatorType):
    def __init__(self, symbol):
        self.symbol = symbol
        self.previousDayData: List
        self.lastCandle: Dict[Any, Any] = {}
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
    def run(self, candle: Dict[Any, Any]):
        HLC = self.getHLC(datetime.fromtimestamp(candle["datetime"] / 1000))

        if not HLC["close"]:
            return Actions.NONE
        elif not self.lastCandle:
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
                datetime.fromtimestamp(candle["datetime"] / 1000).isoformat(" "),
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
        # TODO Don't re-request unless its a new day

        c = getClient()
        r = c.get_price_history(
            self.symbol,
            end_datetime=currentTime,
            frequency_type=client.Client.PriceHistory.FrequencyType.DAILY,
            period_type=client.Client.PriceHistory.PeriodType.MONTH,
        )

        assert r.status_code == 200, r.raise_for_status()
        res = r.json()

        # Make sure we get the right candle, timestamp > 24 hours old
        current = len(res["candles"]) - 1
        while (
            datetime.now().timestamp() - (res["candles"][current]["datetime"] / 1000)
            < 86400
        ):
            current -= 1

        self.HLC = res["candles"][current]
        return self.HLC
