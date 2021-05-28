"""
from autoTraders.backtestTrader import BacktestTrader
from tradeTypes.paperTradeStock import PaperTradeStock
from indicators.pivotPoints import PivotPoints
from datetime import datetime
from dataAPIs.alpaca import AlpacaDataAPI
"""

from sentiment_apis import twitter


def main():
    # BACKTESTING
    """
    traders = [
        BacktestTrader(
            PaperTradeStock("FB", 0, 100.1),
            PivotPoints("FB", AlpacaDataAPI()),
            AlpacaDataAPI(),
            datetime(2021, 4, 5, 9),
            datetime(2021, 5, 5, 9),
        )
    ]

    # LIVE PAPER TRADING
    # traders = [
    #   Trader(PaperTradeStock('SPY'), PivotPoints('SPY'), False)
    # ]
    #BacktestTrader.start_traders(traders)
    """

    query = "Dogecoin"
    api = twitter.twitterAPI()
    api.search_for_hashtags(query)
    api.print_tweets()


if __name__ == "__main__":
    main()
