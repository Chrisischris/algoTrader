from typing import Any, Dict, Iterable, List
import talib
import numpy
from auth.const import Actions
from indicators.indicatorType import IndicatorType

# FIXME Not Ready for live trading -> Switch to new data responsibilities
class MomentumSMA(IndicatorType):

  def __init__(self, aggregationMinutes: int, MOMperiod: int, SMAperiod: int):
    self.aggregationMinutes = aggregationMinutes
    self.MOMperiod = MOMperiod
    self.SMAperiod = SMAperiod

  # momentumSMA based trade signals, return BUY, SELL
  def run(self, candle: Dict[Any, Any]):
    # TODO trim data
    # close = self.handleData(candles)
    # Temp to pass lint
    close = 0
  
    if (len(close) < max(self.MOMperiod, self.SMAperiod) * 2):
      return Actions.NONE

    realMOM = talib.MOM(close, timeperiod=self.MOMperiod)
    realSMA = talib.SMA(realMOM, timeperiod=self.SMAperiod)

    realMOM = [x for x in realMOM if str(x) != 'nan']
    realSMA = [x for x in realSMA if str(x) != 'nan']

    lastMOM = len(realMOM) - 1
    lastSMA = len(realSMA) - 1

    prevDiff = realMOM[lastMOM - 1] < realSMA[lastSMA - 1]
    diff = realMOM[lastMOM] < realSMA[lastSMA]
    if (prevDiff and not diff):
      # - to + BUY
      return Actions.BUY
    elif (not prevDiff and diff):
      # + to - SELL
      return Actions.SELL
    else:
      return Actions.NONE

  # Convert to close array
  def handleData(self, candles: List[Dict[Any, Any]]) -> Any:
    tmp = numpy.array([])

    for i in range(0, len(candles), self.aggregationMinutes):
      tmp = numpy.append(tmp, [candles[i]['close']])

    if tmp[len(tmp) - 1] != candles[len(candles) - 1]['close']:
      tmp = numpy.append(tmp, [candles[len(candles) - 1]['close']])

    return tmp

