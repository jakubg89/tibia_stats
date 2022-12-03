# Collecting data from tibia.com by tibiadata.com API
import requests


# headers from tibiadata.com
def headers():
    headers_api = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    return headers_api


def request(url):
    r = requests.get(url, headers=headers()).json()
    return r


# collecting news tickers from last 90 days
def get_ticker_history():
    url = 'https://api.tibiadata.com/v3/news/newsticker'
    history = request(url)
    return history['news']


# collect specific news
def get_specific_news(id_news):
    url = f'https://api.tibiadata.com/v3/news/id/{id_news}'
    news = request(url)
    return news['news']