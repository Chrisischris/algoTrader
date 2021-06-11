import datetime

from sentiment_apis.backtestSentiment import backtester

# from sentiment_apis.twintSearch import twintSearcher

start = datetime.datetime(2021, 5, 1, 0, 0, 0)
end = datetime.datetime(2021, 5, 10, 0, 0, 0)

backtester("AAPL", start, end)

# t = twintSearcher()
# tweets = t.get_tweets_term("AAPL", start, end)
# print(tweets.get_tweets_time(teststart, testend))
