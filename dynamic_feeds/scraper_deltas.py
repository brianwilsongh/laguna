scraper_deltas = {
    "seeking_alpha": {
        "url": 'https://seekingalpha.com/symbol/{0}?s={0}',
        "link_container_class": 'symbol_articles_list',
        "link_container_id": None,
        "blocked_url_fragments": ["/author/*/articles"]
    },
    "nasdaq": {
        "url": 'https://www.nasdaq.com/symbol/{0}/news-headlines',
        "link_container_class": 'news-headlines',
        "link_container_id": None,
        "blocked_url_fragments": ["/author/*", "news-headlines?page="]
    },
    "yahoo": {
        "url": 'https://finance.yahoo.com/quote/{0}/news?p={0}',
        "link_container_class": None,
        "link_container_id": 'latestQuoteNewsStream-0-Stream-Proxy',
        "blocked_url_fragments": []
    }
}
