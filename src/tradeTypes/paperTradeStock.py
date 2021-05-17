from typing import Any, Dict
from auth.const import Actions
from tradeTypes.tradeType import TradeType
from .helpers import isAfterHours, trailingStopLoss, takeProfit
from outputHelpers.CSVBuilder import CSVBuilder


class PaperTradeStock(TradeType):
    def __init__(self, symbol: str, TSLPercent: float = 0, TPPercent: float = 0):
        self._symbol = symbol
        self.balance = 0
        self.inPosition = False

        self.purchasePrice = 0
        self.positionHigh = 0
        self.TSLPercent = TSLPercent
        self.TPPercent = TPPercent

        self.queueSell = False
        self.CSVBuilder = CSVBuilder(
            ["Action", "Price", "P/L", "Balance", "Date"], "PaperTradeStock " + symbol
        )

    @property
    def symbol(self):
        return self._symbol

    def handle(self, res: Actions, currentCandle: Dict[Any, Any]):
        afterHours = isAfterHours(currentCandle.name)

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
        elif not self.TSLPercent == 0 and not afterHours and self.inPosition:
            if (
                trailingStopLoss(
                    float(currentCandle["close"]), self.positionHigh, self.TSLPercent
                )
                == Actions.SELL
            ):
                print("Trailing Stop Loss Triggered")
                self.sell(currentCandle)
        elif not self.TPPercent == 0 and not afterHours and self.inPosition:
            if (
                takeProfit(
                    float(currentCandle["close"]), self.purchasePrice, self.TPPercent
                )
                == Actions.SELL
            ):
                print("Take Profit Triggered")
                self.sell(currentCandle)

        if self.inPosition and currentCandle["close"] > self.positionHigh:
            self.positionHigh = currentCandle["close"]

    def buy(self, currentCandle: Dict[Any, Any]):
        if not self.inPosition:
            self.inPosition = True
            self.purchasePrice = currentCandle["close"]
            self.positionHigh = currentCandle["close"]
            self.CSVBuilder.write(
                [
                    "Bought",
                    currentCandle["close"],
                    0,
                    "{0:.2f}".format(self.balance),
                    currentCandle.name.isoformat(" "),
                ]
            )

    def sell(self, currentCandle: Dict[Any, Any]):
        if self.inPosition:
            self.inPosition = False
            PL = currentCandle["close"] - self.purchasePrice
            self.balance += PL
            self.CSVBuilder.write(
                [
                    "Sold",
                    currentCandle["close"],
                    "{0:.2f}".format(PL),
                    "{0:.2f}".format(self.balance),
                    currentCandle.name.isoformat(" "),
                ]
            )
