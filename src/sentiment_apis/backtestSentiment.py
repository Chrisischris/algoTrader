import datetime
from sentiment_apis.sentimentAnalyzer import NLTKsentimentAnalyzer
from sentiment_apis.twintSearch import twintSearcher
import csv


def backtester(term: str, start: datetime, end: datetime):
    file = open("output/SentimentTrade" + term + ".csv", "w")
    writer = csv.writer(file)
    header = ["Start", "End", "Sentiment Score"]
    writer.writerow(header)
    searcher = twintSearcher()
    tweets = searcher.get_tweets_term(term, start, end)
    analyzer = NLTKsentimentAnalyzer(tweets)
    delta = datetime.timedelta(hours=1)

    while start < end:
        next = start + delta
        writer.writerow([start, next, analyzer.evaluate(start, next)])

        start = next
        next += delta

    file.close()
