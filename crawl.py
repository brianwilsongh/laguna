from splinter import Browser
from bs4 import BeautifulSoup
from bs4.element import Comment
import re
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import numpy as np

MIN_PARAGRAPH_WORD_LENGTH = 15

def process_element(element): #return text from a <p> tag meeting criteria to inclusion into corpus
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]', 'a'] or isinstance(element, Comment): 
        return "" #filter out txt from hidden elements or comments
    if element.parent.name in ['p']:
        txt = alphanum(element.strip())
        if len(txt) > 0:
            words = TextBlob(txt).words
            if len(words) >= MIN_PARAGRAPH_WORD_LENGTH and not "©" in words:
                print(f"TXT: {txt}")
                return txt + "\n"
    return ""
    
def alphanum(str):
    if re.compile('.*[a-z]+.*').match(str):
        return str
    return ""


urls = []
urls.append("http://www.marketwatch.com")
urls.append("https://www.marketwatch.com/story/after-earnings-barrage-and-data-stock-market-moves-now-hinge-on-global-trade-2018-05-05")
urls.append("https://finance.yahoo.com/")
urls.append("https://stackoverflow.com/questions/4990718/python-about-catching-any-exception")
urls.append('https://webonastick.com/php.html')
laguna_map = {}
# with Browser('firefox', headless=True) as browser:
try:
    browser = Browser('firefox', headless=True)
    for url in urls:
        try:
            browser.visit(url)
            page_corpus = ""
            for element in BeautifulSoup(browser.html, 'html.parser').findAll(text=True):
                page_corpus += process_element(element)
            # for link in soup.find_all('a'): #prints all urls as attrs of <a> tags
            #     print(link.get('href'))
            print("\n\nALL_TEXT\n\n")
            print(page_corpus)
            
            blob = TextBlob(page_corpus)
            polarity = blob.sentiment.polarity #-1 to 1, 1 being positive
            subjectivity = blob.sentiment.subjectivity #0 to 1, 1 being subjective
            # print(f"polarity (aggregated) : {total_polarity}")
            laguna_map[url] = [polarity, subjectivity]
        except:
            laguna_map[url] = None
finally:
    browser.quit()
    for url, features in laguna_map.items():
        print(url)
        if features != None: print(f"Polarity:{features[0]}  Subjectivity:{features[1]}")
    
    
    
    
    
    
    
    
    
    
    
    
    
    