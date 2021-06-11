from datetime import datetime
from nltk.sentiment import SentimentIntensityAnalyzer
import re
from sentiment_apis.models.Tweets import Tweets
from pandas import DataFrame


# Removes links and tags
def clean_tweet(tweet):
    return tweet.join(
        re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()
    )


class NLTKsentimentAnalyzer:
    def __init__(self, tweets: Tweets):
        self.analyzer = SentimentIntensityAnalyzer()
        self.tweets = tweets
        self.average = 0

    def set_tweets(self, tweets: Tweets):
        self.tweets = tweets

    def get_all_tweets(self):
        return self.tweets.get_tweets()

    def get_score(self, input: str):
        return self.analyzer.polarity_scores(input)["compound"]

    def get_average(self, df):
        total = 0
        for index, row in df.iterrows():
            total += self.get_score(clean_tweet(row["tweet"]))

        return total / self.tweets.size

    def get_decision(self, df: DataFrame):
        compound = self.get_average(df)
        self.average = compound
        return compound

    def evaluate(self, start: datetime, end: datetime):
        df = self.tweets.get_tweets_time(start, end)
        return self.get_decision(df)
