# Collecting data from tibia.com by tibiadata.com API
import requests


# headers from tibiadata.com
def headers():
    headers_api = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    return headers_api


def request(url):
    r = requests.get(url, headers=headers()).json()
    return r


# # # # # # # News ticker # # # # # # #

# collecting news tickers from last 90 days
def get_ticker_history():
    url = 'https://api.tibiadata.com/v3/news/newsticker'
    ticker_history = request(url)
    return ticker_history['news']


# collect specific news or ticker
def get_specific_news(id_news):
    url = f'https://api.tibiadata.com/v3/news/id/{id_news}'
    news = request(url)
    return news['news']

# # # # # # # News ticker end # # # # # # #


# # # # # # # News # # # # # # #

def get_news_history():
    url = 'https://api.tibiadata.com/v3/news/latest'
    news_history = request(url)
    return news_history['news']

# # # # # # # News end # # # # # # #


# # # # # # # Boosted creature/boss # # # # # # #

# get boosted boss
def boosted_boss():
    url = 'https://api.tibiadata.com/v3/boostablebosses'
    news = request(url)
    return news['boostable_bosses']['boosted']


# get boosted boss
def boosted_creature():
    url = 'https://api.tibiadata.com/v3/creatures'
    news = request(url)
    return news['creatures']['boosted']

# # # # # # # Boosted creature/boss end # # # # # # #
