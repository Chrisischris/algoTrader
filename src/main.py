from autoTraders.trader import start_traders, Trader
from autoTraders.tradeTypes.paperTradeStock import PaperTradeStock
from indicators.pivotPoints import PivotPoints
from datetime import date, datetime, timedelta


def main():
    # BACKTESTING
    traders = [
        Trader(
            PaperTradeStock("FB", 0, 100.1),
            PivotPoints("FB"),
            True,
            datetime(2020, 11, 5, 9),
            datetime(2020, 12, 26, 9),
        )
    ]

    # LIVE PAPER TRADING
    # traders = [
    #   Trader(PaperTradeStock('SPY'), PivotPoints('SPY'), False)
    # ]

    # start_traders(traders)

    PivotPoints("TSLA").getHLC(datetime.now())


if __name__ == "__main__":
    main()
