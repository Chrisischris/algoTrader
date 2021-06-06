def create_db():
    d = {}
    file = open("src/sentiment_apis/stockDatabase/stocks.txt")
    for line in file:
        line = line.strip().split("-")
        d[line[0]] = line[1]

    return d


db = create_db()
print(db)
