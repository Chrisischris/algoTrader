# Temporary file to test twint.
import datetime

from sentiment_apis.twintSearch import twitterSearch

from sentiment_apis.sentimentAnalyzer import NLTKsentimentAnalyzer

import pandas

pandas.set_option("display.max_rows", None, "display.max_columns", None)

searcher = twitterSearch()

start = datetime.datetime(2021, 4, 1, 0, 0, 0)

end = datetime.datetime(2021, 4, 1, 0, 0, 0)


print(start, end)

data = searcher.get_tweets_term("bitcoin", start, end, 3)
print(data)

# print(data)
analyzer = NLTKsentimentAnalyzer(data)

decision = analyzer.get_decision()
print(analyzer.average)
print(decision)
