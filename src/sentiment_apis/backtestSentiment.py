import datetime
from sentiment_apis.sentimentAnalyzer import NLTKsentimentAnalyzer
from sentiment_apis.twintSearch import twintSearcher
import csv

TIME_INTERVAL_DELTA = datetime.timedelta(minutes=1)
SENTIMENT_RESET = 360  # reset sentiment every 6 hours


def backtester(term: str, start: datetime, end: datetime):
    file = open("output/SentimentTrade" + term + ".csv", "w")
    writer = csv.writer(file)
    header = ["Start", "End", "Sentiment Score"]
    writer.writerow(header)
    searcher = twintSearcher()
    tweets = searcher.get_tweets_term(term, start, end)
    analyzer = NLTKsentimentAnalyzer(tweets)

    while start < end:
        next = start + TIME_INTERVAL_DELTA
        writer.writerow([start, next, analyzer.evaluate(start, next)])
        start = next
        next += TIME_INTERVAL_DELTA

    file.close()
