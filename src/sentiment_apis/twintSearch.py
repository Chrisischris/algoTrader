import twint
from datetime import datetime
from sentiment_apis.models.Tweets import Tweets


class twintSearcher:
    def get_tweets_term(self, term, start_date: datetime, end_date: datetime):
        start = start_date.strftime("%Y-%m-%d")
        end = end_date.strftime("%Y-%m-%d")
        config = twint.Config()
        config.Pandas = True
        config.Hide_output = True
        config.Search = "(" + term + ")" + " until:" + end + " since:" + start
        config.Lang = "en"
        twint.run.Search(config)
        tweets_df = twint.storage.panda.Tweets_df
        df = self.build_df(tweets_df)
        return Tweets(df)

    def build_df(self, df):
        df = df[df["language"] == "en"]
        df = df[["username", "tweet", "date"]]
        return df
