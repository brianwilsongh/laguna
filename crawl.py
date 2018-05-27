from splinter import Browser
import numpy as np
import utils

def init(urls):
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
