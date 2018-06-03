from bs4 import BeautifulSoup
from bs4.element import Comment
import re
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from fnmatch import fnmatch

import time

def analyze_text(corpus):
    blob = TextBlob(corpus)
    polarity = blob.sentiment.polarity #-1 to 1, 1 being positive
    subjectivity = blob.sentiment.subjectivity #0 to 1, 1 being subjective
    print(f'polarity(-1 -> 1):{polarity}, subjectivity(0 -> 1):{subjectivity}')
    return [polarity, subjectivity]

def process_page(html):
    page_corpus = ""
    for element in BeautifulSoup(html, 'html.parser').findAll(text=True):
        page_corpus += process_element(element)
    return page_corpus


def process_element(element, options): #return text from a <p> tag meeting criteria to inclusion into corpus
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]', 'a'] or isinstance(element, Comment):
        return "" #filter out txt from hidden elements or comments
    if element.parent.name in ['p', 'div']:
        txt = alphanum(element.strip())
        if len(txt) > 0:
            words = TextBlob(txt).words
            if len(words) >= options['MIN_PARAGRAPH_WORD_LENGTH'] and not "©" in words:
                print(f"TXT: {txt}")
                time.sleep(1)
                return txt + "\n"
    return ""

def alphanum(str):
    if re.compile('.*[a-z]+.*').match(str):
        return str
    return ""

def link_matches_blocklist(link, blocklist):
    for block in blocklist:
        if fnmatch(link, block): return True
    return False

def ensure_full_url(link, origin):
    # return "must implement utils.ensure_full_url" TODO: implement this
    return link
