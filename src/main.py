from autoTraders.trader import start_traders, Trader
from autoTraders.tradeTypes.paperTradeStock import PaperTradeStock
from indicators import momentumSMA
from datetime import datetime, timedelta

def main():
  traders = [Trader(PaperTradeStock('TSLA'), momentumSMA.MomentumSMA(60, 14, 28), True, datetime.now() - timedelta(days=90))]
  #traders = [Trader(PaperTradeStock('TSLA'), macd.MACD())]
  start_traders(traders)


if __name__ == "__main__":
  main()