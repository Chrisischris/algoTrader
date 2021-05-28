from sentiment_apis.twint_test import twitterSearch
from sentiment_apis.sentiment_analysis import sentimentAnalyzer

searcher = twitterSearch()
data = searcher.get_tweets_term("dogecoin")


analyzer = sentimentAnalyzer(data)
decision = analyzer.get_decision()

print(analyzer.average)
print(decision)