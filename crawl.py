from splinter import Browser
import numpy as np
import utils

urls = []
urls.append("https://www.cnbc.com/2018/05/24/crowdstrikes-security-platform-could-someday-attract-amazon-google.html")
urls.append("http://www.marketwatch.com")
urls.append("http://money.cnn.com/")
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
            print(f'visiting {url}')
            browser.visit(url)
            print(f'processing page of {url}')
            laguna_map[url] = utils.analyze_text(utils.process_page(browser.html))
        except Exception as e:
            print("Error!")
            print(e)
            laguna_map[url] = None
except Exception as e:
    print(e)
finally:
    browser.quit()
    for url, features in laguna_map.items():
        print(url)
        if features != None: print(f"Polarity:{features[0]}  Subjectivity:{features[1]}")
