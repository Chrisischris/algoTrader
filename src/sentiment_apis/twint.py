import twint
import pandas


class twitterSearch:
    def get_tweets_term(self, term):
        config = twint.Config()
        config.Search = term
        config.Lang = "en"
        config.Limit = 100
        config.Hide_output = True
        config.Store_csv = True
        output = "src/sentiment_apis/tweetCSVs/" + term + ".csv"
        config.Output = output
        twint.run.Search(config)

        df = pandas.read_csv(config.Output, usecols=["username", "tweet", "language"])

        eng_df = df[df["language"] == "en"]

        del eng_df["language"]

        return eng_df
