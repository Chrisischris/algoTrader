import twint
from datetime import datetime, timedelta
import re

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

    def clean_tweet(self, tweet):
        return tweet.join(
            re.sub(
                "(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet
            ).split()
        )


searcher = twitterSearch()
start = datetime(2021, 4, 1, 0, 0, 0)  # 4/1/2021 00:00:00
end = datetime(2021, 4, 1, 0, 0, 0)  # 5/1/2021 00:00:00
data = searcher.get_tweets_term("bitcoin", start, end, 3)
