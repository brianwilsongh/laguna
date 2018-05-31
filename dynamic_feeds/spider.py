from splinter import Browser
import numpy as np
import utils
from dynamic_feeds.scraper_deltas import deltas as scraper_deltas
from dynamic_feeds.rss_deltas import deltas as rss_deltas
from bs4 import BeautifulSoup
import newspaper
import time
from fnmatch import fnmatch
from newspaper import Article
from datetime import datetime, timedelta

class Spider:
    def __init__(self, data, options):
        print("Finder has been initialized")
        try:
            self.browser = Browser('firefox', headless=True, incognito=True, capabilities={'acceptSslCerts': True, 'javascriptEnabled': True, })
        except Exception as e:
            print(e)
            print(f'Failed to initialize browser for Spider {self}')
        self.aggregate_data = data
        self.options = options

    def crawl_rss(self, sym):
        for source in rss_deltas:
            try:
                rss_feed = rss_deltas[source]
                for entry in feedparser.parse(rss_feed).entries:
                    print(entry.published_parsed)
                    print(entry.link)

                    if not entry.link in aggregate_data[symbol]:
                        article = Article(entry.link)
                        article_count += 1
                        article.download()
                        article.parse()
                        if ((datetime.today() - timedelta(days=ARTICLE_EXPIRATION_TIMEDELTA)).date()) <= article.publish_date.date():
                            self.aggregate_data[symbol][entry.link] = utils.analyze_text(article.text)
                            # print(aggregate_data)
                        print("\n")
                    else:
                        print("DUPLICATE ARTICLE FOUND VIA RSS")
            except Exception as e:
                print(e)
                print("Moving on after failing to retrieve from src:", source)
                continue
        return self.aggregate_data

    def crawl_direct(self, sym):
        for source in scraper_deltas:
            try:
                info = deltas[source]
                print(f'\nSpider direct crawl from src: {source}')
                print('going to', info['url'].format(sym))
                self.browser.visit(info['url'].format(sym))
                soup = BeautifulSoup(self.browser.html, 'html.parser')

                link_containing_element = soup.find(class_=info['link_container_class']) if info['link_container_class'] != None else soup.find(id=info['link_container_id'])
                links = link_containing_element.find_all('a')
                print("links from ", info['url'].format(sym))
                for a in links:
                    if not a.get('href', None) == None and not self.link_matches_blocklist(a['href'], info['blocked_url_fragments']):
                        print("href=", a['href'])
                # for element in BeautifulSoup(self.browser.html, 'html.parser').findAll(text=True): #alter to find element containing relevant <a>
                #     #find all children <a> tags,
                #     for link in links:
                #         self.browser.visit(link)
                #         self.aggregate_data[info['url']] = utils.analyze_text(utils.process_page(browser.html))
            except Exception as e:
                print(e)
                print("Moving on after failing to retrieve from src:", source)
                continue
        return self.aggregate_data

    def link_matches_blocklist(self, link, blocklist):
        for block in blocklist:
            if fnmatch(link, block): return True
        return False
