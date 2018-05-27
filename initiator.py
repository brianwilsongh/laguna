import feedparser
import json
from newspaper import Article
from datetime import datetime
import utils

ticker_symbols = ['TGT', 'XLE', 'WMT']

aggregate_data = {}

for symbol in ticker_symbols:
    aggregate_data[symbol] = {}

    rss_feeds = []
    rss_feeds.append(f'http://articlefeeds.nasdaq.com/nasdaq/symbols?symbol={symbol}')
    for rss_feed in rss_feeds:
        try:
            for entry in feedparser.parse(rss_feed).entries:
                print(entry.published_parsed)
                print(entry.link)

                if not entry.link in aggregate_data[symbol]:
                    article = Article(entry.link)
                    article.download()
                    article.parse()
                    aggregate_data[symbol][entry.link] = utils.analyze_text(article.text)
                    print(article.authors)
                    print(article.publish_date.date())
                    print(datetime.today().date())
                    print(f'equal? {datetime.today().date() == article.publish_date.date()}')
                    print("\n\n")
                    print(aggregate_data)
        except Exception as e:
            print(e)
            print("Moving to next...")
            continue
