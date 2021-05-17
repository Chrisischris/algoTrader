from autoTraders.backtestTrader import BacktestTrader
from tradeTypes.paperTradeStock import PaperTradeStock
from indicators.pivotPoints import PivotPoints
from datetime import datetime
from dataAPIs.alpaca import AlpacaDataAPI


def main():
    # BACKTESTING
    traders = [
        BacktestTrader(
            PaperTradeStock("FB", 0, 100.1),
            PivotPoints("FB", AlpacaDataAPI()),
            AlpacaDataAPI(),
            datetime(2021, 4, 5, 9),
            datetime(2021, 5, 5, 8),
        )
    ]

    # LIVE PAPER TRADING
    # traders = [
    #   Trader(PaperTradeStock('SPY'), PivotPoints('SPY'), False)
    # ]

    BacktestTrader.start_traders(traders)


if __name__ == "__main__":
    main()
