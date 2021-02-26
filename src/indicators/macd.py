from typing import Dict
import talib
import numpy
from auth.const import Actions
from indicators.indicatorType import IndicatorType

# FIXME Not Ready for live trading -> Switch to new data responsibilities
class MACD(IndicatorType):
  # MACD based trade signals, return BUY, SELL
  def run(self, candle: Dict[Any, Any]):
    close = self.handleData(candles)
    macd, macdsignal, macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)

    last = len(macdhist) - 1
    if (macdhist[last - 1] < 0 and macdhist[last] >= 0):
      # - to + BUY
      return Actions.BUY
    elif (macdhist[last - 1] >= 0 and macdhist[last] < 0):
      # + to - SELL
      return Actions.SELL
    else:
      return Actions.NONE

  # Convert to close array
  def handleData(self, candles: Iterable[Dict]):
    tmp = numpy.array([])
    for c in candles:
      tmp = numpy.append(tmp, [c['close']])
    return tmp

