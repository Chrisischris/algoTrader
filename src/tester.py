# Temporary file to test twint.

from sentiment_apis.twintSearch import twitterSearch

from sentiment_apis.sentimentAnalyzer import sentimentAnalyzer


searcher = twitterSearch()

start = "2021-04-03 13:30:00"
end = "2021-04-03 20:00:00"

data = searcher.get_tweets_term("bitcoin", start, end, 100)

# print(data)
analyzer = sentimentAnalyzer(data)

decision = analyzer.get_decision()
print(analyzer.average)
print(decision)
