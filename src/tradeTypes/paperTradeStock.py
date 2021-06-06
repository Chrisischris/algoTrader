from pandas.core.series import Series
from auth.const import Actions
from tradeTypes.tradeType import TradeType
from .helpers import is_after_hours, trailing_stop_loss, take_profit
from outputHelpers.CSVBuilder import CSVBuilder


class PaperTradeStock(TradeType):
    def __init__(
        self,
        symbol: str,
        tsl_percent: float = 0,
        tp_percent: float = 0,
        output: bool = False,
        **kwargs
    ):
        self._symbol = symbol
        self.balance = 0
        self.in_position = False

        self.purchase_price = 0
        self.position_high = 0
        self.tsl_percent = tsl_percent
        self.tp_percent = tp_percent

        self.queue_sell = False

        self.output = output
        if self.output:
            self.csv_builder = CSVBuilder(
                ["Action", "Price", "P/L", "Balance", "Date"],
                "PaperTradeStock " + symbol,
            )

    @property
    def symbol(self):
        return self._symbol

    def handle(self, res: Actions, current_bar: Series):
        after_hours = is_after_hours(current_bar.name)

        if res == Actions.BUY and not after_hours:
            self.buy(current_bar)
        elif res == Actions.SELL:
            if after_hours:
                self.queue_sell = True
            else:
                self.sell(current_bar)
        elif self.queue_sell and not after_hours:
            # TODO check if you should still sell
            self.sell(current_bar)
            self.queue_sell = False
        # IMPROVEMENT: Do stop losses change from after hours data?
        elif not self.tsl_percent == 0 and not after_hours and self.in_position:
            if (
                trailing_stop_loss(
                    float(current_bar["close"]), self.position_high, self.tsl_percent
                )
                == Actions.SELL
            ):
                self.sell(current_bar)
        elif not self.tp_percent == 0 and not after_hours and self.in_position:
            if (
                take_profit(
                    float(current_bar["close"]), self.purchase_price, self.tp_percent
                )
                == Actions.SELL
            ):
                self.sell(current_bar)

        if self.in_position and current_bar["close"] > self.position_high:
            self.position_high = current_bar["close"]

        return self.balance

    def buy(self, bar: Series):
        if not self.in_position:
            self.in_position = True
            self.purchase_price = bar["close"]
            self.position_high = bar["close"]
            if self.output:
                self.csv_builder.write(
                    [
                        "Bought",
                        bar["close"],
                        0,
                        "{0:.2f}".format(self.balance),
                        bar.name.isoformat(" "),
                    ]
                )

    def sell(self, bar: Series):
        if self.in_position:
            self.in_position = False
            pl = bar["close"] - self.purchase_price
            self.balance += pl
            if self.output:
                self.csv_builder.write(
                    [
                        "Sold",
                        bar["close"],
                        "{0:.2f}".format(pl),
                        "{0:.2f}".format(self.balance),
                        bar.name.isoformat(" "),
                    ]
                )
