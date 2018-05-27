import feedparser
import json
from newspaper import Article

ticker_symbols = ['TGT', 'XLE', 'WMT']

for symbol in ticker_symbols:
    rss = f'http://articlefeeds.nasdaq.com/nasdaq/symbols?symbol={symbol}'
    data = feedparser.parse(rss)
    for entry in data.entries:
        print(entry.published_parsed)
        print(entry.link)
        article = Article(entry.link)
        article.download()
        article.parse()
        print(article.authors)
        print(article.publish_date)
        print(article.text)
        print("\n\n")
