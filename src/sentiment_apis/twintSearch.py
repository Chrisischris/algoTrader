from numpy import datetime_as_string
import twint


class twitterSearch:
    def get_tweets_term(self, term, start_date, end_date, limit):
        start = datetime_as_string(start_date)
        end = datetime_as_string(end_date)
        config = twint.Config()
        config.Pandas = True
        config.Hide_output = True
        config.Search = term
        config.Lang = "en"
        config.Limit = limit
        config.Since = start
        config.Until = end
        twint.run.Search(config)
        tweets_df = twint.storage.panda.Tweets_df
        print(tweets_df)

        print(tweets_df[["date"]])

        return self.build_df(tweets_df)

    def build_df(self, df):
        df = df[df["language"] == "en"]
        df = df[["username", "tweet"]]

        return df
