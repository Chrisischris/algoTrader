# Temporary file to test twint.

from sentiment_apis.twint import twitterSearch
from sentiment_apis.sentimentAnalyzer import sentimentAnalyzer

searcher = twitterSearch()
data = searcher.get_tweets_term("dogecoin")


analyzer = sentimentAnalyzer(data)
decision = analyzer.get_decision()

print(analyzer.average)
print(decision)