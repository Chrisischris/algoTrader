from datetime import datetime, timedelta
from sentiment_apis.sentimentAnalyzer import NLTKsentimentAnalyzer
from sentiment_apis.twintSearch import twintSearcher
from dataAPIs.alpaca import AlpacaDataAPI
from alpaca_trade_api.rest import TimeFrame
from pandas import Series
import csv

TIME_INTERVAL_DELTA = timedelta(minutes=1)
SENTIMENT_RESET = 360  # reset sentiment every 6 hours
SENTIMENT_BUY = 0.1
SENTIMENT_SELL = 0


def backtester(term: str, start: datetime, end: datetime):
    api = AlpacaDataAPI()
    bars = api.get_bars_timeframe(term, TimeFrame.Minute, start, end).get_bars()
    file = open("output/SentimentTrade" + term + ".csv", "w")
    writer = csv.writer(file)
    header = ["Start", "End", "Price", "Sentiment Score"]
    writer.writerow(header)
    searcher = twintSearcher()

    tweets = searcher.get_tweets_term(term, start, end)
    analyzer = NLTKsentimentAnalyzer(tweets)

    count = 0
    prev = None
    sentiment = 0
    tweet_count = 0

    for index, bar in bars.iterrows():
        time = get_time_bar(bar)
        price = bar["open"]
                
        if count >= 1:
            results = analyzer.evaluate(prev, time)
            sentiment += results[0]
            tweet_count += results[1]

            average = sentiment / tweet_count
            writer.writerow([start, end, price, average])
                 
        prev = time
        count += 1

    file.close()


# TODO figure out strptime
def get_time_bar(bar: Series):
    tmp = str(bar.name).split()
    part1 = tmp[0].strip().split("-")
    part2 = tmp[1].strip().split("+")[0].split(":")
    date = datetime(
        int(part1[0]),
        int(part1[1]),
        int(part1[2]),
        int(part2[0]),
        int(part2[1]),
        int(part2[2]),
    )
    return date
