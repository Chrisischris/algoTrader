import twint


class twitterSearch:
    def get_tweets_term(self, term, start_date, end_date, limit):
        config = twint.Config()
        config.Pandas = True
        config.Hide_output = True
        config.Search = term
        config.Lang = "en"
        config.Limit = limit
        # config.Since = start_date
        config.Until = end_date
        twint.run.Search(config)
        tweets_df = twint.storage.panda.Tweets_df
        print(tweets_df)

        print(tweets_df[["date"]])

        return self.build_df(tweets_df)

    def build_df(self, df):
        df = df[df["language"] == "en"]
        df = df[["username", "tweet"]]

        return df
