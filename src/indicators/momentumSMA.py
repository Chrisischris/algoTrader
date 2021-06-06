from typing import Any, Dict, List
import talib
import numpy
from auth.const import Actions
from indicators.indicatorType import IndicatorType


# FIXME Not Ready for live trading -> Switch to new data responsibilities
class MomentumSMA(IndicatorType):
    def __init__(self, aggregation_minutes: int, mom_period: int, sma_period: int):
        self.aggregation_minutes = aggregation_minutes
        self.mom_period = mom_period
        self.sma_period = sma_period

    # momentumSMA based trade signals, return BUY, SELL
    def run(self, candle: Dict[Any, Any]):
        # TODO trim data
        # close = self.handle_data(candles)
        # Temp to pass lint
        close = 0

        if len(close) < max(self.mom_period, self.sma_period) * 2:
            return Actions.NONE

        real_mom = talib.MOM(close, timeperiod=self.mom_period)
        real_sma = talib.SMA(real_mom, timeperiod=self.sma_period)

        real_mom = [x for x in real_mom if str(x) != "nan"]
        real_sma = [x for x in real_sma if str(x) != "nan"]

        last_mom = len(real_mom) - 1
        last_sma = len(real_sma) - 1

        prev_diff = real_mom[last_mom - 1] < real_sma[last_sma - 1]
        diff = real_mom[last_mom] < real_sma[last_sma]
        if prev_diff and not diff:
            # - to + BUY
            return Actions.BUY
        elif not prev_diff and diff:
            # + to - SELL
            return Actions.SELL
        else:
            return Actions.NONE

    # Convert to close array
    def handle_data(self, candles: List[Dict[Any, Any]]) -> Any:
        tmp = numpy.array([])

        for i in range(0, len(candles), self.aggregation_minutes):
            tmp = numpy.append(tmp, [candles[i]["close"]])

        if tmp[len(tmp) - 1] != candles[len(candles) - 1]["close"]:
            tmp = numpy.append(tmp, [candles[len(candles) - 1]["close"]])

        return tmp
