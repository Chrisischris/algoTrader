from pandas import DataFrame
from datetime import datetime


class Tweets:
    def __init__(self, all_tweets: DataFrame):
        self.tweets = all_tweets
        self.tweets["date"] = self.tweets["date"].astype("datetime64[ns]")
        self.size = len(self.tweets)

    def get_all_tweets(self) -> DataFrame:
        return self.tweets

    def get_tweets_time(self, start: datetime, end: datetime):
        tweets = self.tweets[
            (self.tweets["date"] >= start) & (self.tweets["date"] <= end)
        ]
        return tweets, len(tweets)