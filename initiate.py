import feedparser
import json
from newspaper import Article
from datetime import datetime, timedelta
import utils
import crawl
from dynamic_feeds.spider import Spider

options = {}
# options['TICKER_SYMBOLS'] = ['TGT', 'XLE', 'WMT']
options['TICKER_SYMBOLS'] = ['TGT']
options['ARTICLE_EXPIRATION_TIMEDELTA'] = 2 #number of time units within which article is valid relative to current time
options['MIN_PARAGRAPH_WORD_LENGTH'] = 15


aggregate_data = {}

for symbol in options['TICKER_SYMBOLS']:
    aggregate_data[symbol] = {}
    article_count = 0

    spider = Spider(aggregate_data, options)
    
    aggregate_data = spider.crawl(symbol) #TEST

    rss_feeds = []
    rss_feeds.append(f'http://articlefeeds.nasdaq.com/nasdaq/symbols?symbol={symbol}')
    for rss_feed in rss_feeds:
        try:
            for entry in feedparser.parse(rss_feed).entries:
                print(entry.published_parsed)
                print(entry.link)

                if not entry.link in aggregate_data[symbol]:
                    article = Article(entry.link)
                    article_count += 1
                    article.download()
                    article.parse()
                    if ((datetime.today() - timedelta(days=ARTICLE_EXPIRATION_TIMEDELTA)).date()) <= article.publish_date.date():
                        aggregate_data[symbol][entry.link] = utils.analyze_text(article.text)
                        print(aggregate_data)
                    print("\n")
                else:
                    print("DUPLICATE ARTICLE FOUND VIA RSS")
        except Exception as e:
            print(e)
            print("Moving to next...")
            continue
    urls = []
    # crawl.init(urls)
    aggregate_data = Spider(aggregate_data, options).crawl(symbol)


    aggregate_data[symbol]['article_count'] = article_count
