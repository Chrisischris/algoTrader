import twint
from datetime import datetime, timedelta

TIMEDELTA = 2


class twitterSearch:
    def get_tweets_term(self, term, start_date: datetime, end_date: datetime, limit):
        end_date = end_date + timedelta(days=TIMEDELTA)
        start = start_date.strftime("%Y-%m-%d %H:%M:%S")
        end = end_date.strftime("%Y-%m-%d %H:%M:%S")
        config = twint.Config()
        config.Pandas = True
        config.Hide_output = True
        config.Search = term
        config.Lang = "en"
        config.Limit = 10
        config.Since = start
        config.Until = end
        twint.run.Search(config)
        tweets_df = twint.storage.panda.Tweets_df
        print(tweets_df[:1]["date"])
        tweet = tweets_df[:1]["tweet"]
        print(tweet)
        return self.build_df(tweets_df)

    def build_df(self, df):
        df = df[df["language"] == "en"]
        df = df[["username", "tweet"]]
        return df


