from typing import Any, Dict
from auth.const import Actions
from datetime import datetime
from autoTraders.tradeTypes.tradeType import TradeType
from .helpers import isAfterHours, trailingStopLoss
from outputHelpers.CSVBuilder import CSVBuilder

class PaperTradeStock(TradeType):

  def __init__(self, symbol: str, trailingStopLoss: float = 0):
    self._symbol = symbol
    self.balance = 0
    self.inPosition = False
    self.purchasePrice = 0
    self.positionHigh = 0
    self.trailingStopLoss = trailingStopLoss
    self.queueSell = False
    self.CSVBuilder = CSVBuilder(['Action', 'Price', 'Balance', 'Date'], 'PaperTradeStock ' + symbol)

  @property
  def symbol(self):
    return self._symbol

  def handle(self, res: Actions, currentCandle: Dict[Any, Any]):
    afterHours = isAfterHours(currentCandle['datetime'])

    if res == Actions.BUY and not afterHours:
      self.buy(currentCandle)
    elif res == Actions.SELL:
      if afterHours:
        self.queueSell = True
      else:
        self.sell(currentCandle)
    elif self.queueSell and not afterHours:
      # TODO check if you should still sell
      self.sell(currentCandle)
      self.queueSell = False
    # IMPROVEMENT: Do stop losses change from after hours data?
    elif not self.trailingStopLoss == 0 and not afterHours:
      if (trailingStopLoss(float(currentCandle['close']), self.positionHigh, self.trailingStopLoss) == Actions.SELL):
        print('Trailing Stop Loss Triggered')
        self.sell(currentCandle)
  
    if (self.inPosition and currentCandle['close'] > self.positionHigh):
      self.positionHigh = currentCandle['close']

  def buy(self, currentCandle: Dict[Any, Any]):
    if not self.inPosition:
      self.inPosition = True
      self.purchasePrice = currentCandle['close']
      self.positionHigh = currentCandle['close']
      self.CSVBuilder.write(['Bought', currentCandle['close'], "{0:.2f}".format(self.balance), datetime.fromtimestamp(currentCandle['datetime'] / 1000).isoformat(' ')])

  def sell(self, currentCandle: Dict[Any, Any]):
    if self.inPosition:
      self.inPosition = False
      self.balance += currentCandle['close'] - self.purchasePrice
      self.CSVBuilder.write(['Sold', currentCandle['close'], "{0:.2f}".format(self.balance), datetime.fromtimestamp(currentCandle['datetime'] / 1000).isoformat(' ')])
