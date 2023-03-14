import requests
import random
from bs4 import BeautifulSoup
from headers import headers
from scripts.proxy_scrapper.proxy_functions import get_proxy_list


def world():
    worlds = []
    url = "https://www.tibia.com/community/?subtopic=highscores"
    request_headers = headers()
    proxy_list = get_proxy_list()
    random.shuffle(proxy_list)
    proxy = {
        "http": proxy_list[0],
    }
    soup = BeautifulSoup(
        requests.get(url, headers=request_headers, proxies=proxy).text,
        "html.parser",
    )
    for option in soup.find_all("select", {"name": "world"}):
        for i in option.findAll("option"):
            if i["value"] != "":
                worlds.append(i["value"])
    return worlds
