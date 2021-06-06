from nltk.sentiment import SentimentIntensityAnalyzer
import re


# Removes links and tags
def clean_tweet(tweet):
    return tweet.join(
        re.sub(
            "(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet
        ).split()
    )


class NLTKsentimentAnalyzer:
    def __init__(self, posts):
        self.analyzer = SentimentIntensityAnalyzer()
        self.posts = posts
        self.average = 0

    def get_score(self, input):
        return self.analyzer.polarity_scores(input)["compound"]

    def get_average(self):
        total = 0
        for index, row in self.posts.iterrows():
            total += self.get_score(clean_tweet(row["tweet"]))

        return total / len(self.posts)

    def get_decision(self):
        compound = self.get_average()
        self.average = compound
        if compound >= 0.3:
            return "BUY"
        elif compound > -0.3 and compound < 0.3:
            return "HOLD"
        else:
            return "SELL"


