from splinter import Browser
import numpy as np
import utils
from dynamic_feeds.scraper_deltas import deltas
from bs4 import BeautifulSoup
import newspaper
import time
from fnmatch import fnmatch

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

    def crawl(self, sym):
        try:
            for source in deltas:
                info = deltas[source]
                print(f'\nSpider searching for articles from src: {source}')
                print('going to', info['origin'].format(sym))
                self.browser.visit(info['origin'].format(sym))
                soup = BeautifulSoup(self.browser.html, 'html.parser')
                # print(self.browser.evaluate_script('document.readyState'))
                # time.sleep(3)
                # print(self.browser.evaluate_script('document.readyState'))
                # print(soup.find_all(class_="news-headlines"))
                # print(self.browser.find_by_name("news-headlines"))

                link_containing_element = soup.find(class_=info['link_container_class']) if info['link_container_class'] != None else soup.find(id=info['link_container_id'])
                links = link_containing_element.find_all('a')
                print("links from ", info['origin'].format(sym))
                for a in links:
                    if not a.get('href', None) == None and not self.link_matches_blocklist(a['href'], info['blocked_url_fragments']):
                        print("href=", a['href'])
                # for element in BeautifulSoup(self.browser.html, 'html.parser').findAll(text=True): #alter to find element containing relevant <a>
                #     #find all children <a> tags,
                #     for link in links:
                #         self.browser.visit(link)
                #         self.aggregate_data[info['origin']] = utils.analyze_text(utils.process_page(browser.html))
        finally:
            self.browser.quit()
        return self.aggregate_data

    def link_matches_blocklist(self, link, blocklist):
        for block in blocklist:
            if fnmatch(link, block): return True
        return False
