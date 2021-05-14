
from typing import Any, Dict, Iterable
from data_apis.stream import start_stream
from data_apis.request import request
from autoTraders.tradeTypes.tradeType import TradeType
from indicators.indicatorType import IndicatorType
from plot.plot import PricePlot
from datetime import datetime, timedelta
import json

# p = PricePlot()

class Trader:

  def __init__(self, tradeType: TradeType, indicator: IndicatorType, backtest: bool, start: datetime = datetime.now() - timedelta(days=7), end: datetime = datetime.now()):
    self.candles = []
    self.tradeType = tradeType
    self.indicator = indicator
    self.backtest = backtest
    self.start = start
    self.end = end


def start_traders(traders: Iterable[Trader]):
  symbols = []
  for t in traders:
    t.candles = request(t.tradeType.symbol, t.start, t.end)['candles']
    if (t.backtest):
      for c in range(1, len(t.candles)):
        # Get indicator result from data and pass to tradeType to execute
        decision = t.indicator.run(t.candles[c - 1])
        currentCandle = t.candles[c - 1]
        t.tradeType.handle(decision, currentCandle)
    else:
      symbols.append(t.tradeType.symbol)

  if (len(symbols)):
    start_stream(stream_handler, symbols)

def stream_handler(msg: Dict[Any, Any]):
  print(json.dumps(msg, indent=4))
  if 'CLOSE_PRICE' in msg['content'][0]:
    val = msg['content'][0]['CLOSE_PRICE']
    print(val)

    #global p
    #p.add_point(val)