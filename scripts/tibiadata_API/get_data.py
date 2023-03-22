# Collecting data from tibia.com by tibiadata.com API
import requests


# headers from tibiadata.com
def headers():
    headers_api = {
        "content-type": "application/json",
        "Accept-Charset": "UTF-8",
    }
    return headers_api


def request(url):
    r = requests.get(url, headers=headers()).json()
    return r


api_version = "v3"
# # # # # # # News ticker # # # # # # #


# collecting news tickers from last 90 days
def get_ticker_history():
    url = f"https://api.tibiadata.com/{api_version}/news/newsticker"
    ticker_history = request(url)
    return ticker_history["news"]


# collect specific news or ticker
def get_specific_news(id_news):
    url = f"https://api.tibiadata.com/{api_version}/news/id/{id_news}"
    news = request(url)
    return news["news"]


# # # # # # # News ticker end # # # # # # #


# # # # # # # News # # # # # # #


def get_news_history():
    url = f"https://api.tibiadata.com/{api_version}/news/latest"
    news_history = request(url)
    return news_history["news"]


# # # # # # # News end # # # # # # #


# # # # # # # Boosted creature/boss # # # # # # #


# get boosted boss
def boosted_boss():
    url = f"https://api.tibiadata.com/{api_version}/boostablebosses"
    news = request(url)
    return news["boostable_bosses"]["boosted"]


# get boosted boss
def boosted_creature():
    url = f"https://api.tibiadata.com/{api_version}/creatures"
    news = request(url)
    return news["creatures"]["boosted"]


# # # # # # # Boosted creature/boss end # # # # # # #


# # # # # # # Worlds # # # # # # #


# get worlds list with basic information
def get_worlds_information():
    url = f"https://api.tibiadata.com/{api_version}/worlds"
    worlds_info = request(url)
    return worlds_info["worlds"]["regular_worlds"]


def get_world_details(world):
    url = f"https://api.tibiadata.com/{api_version}/world/{world}"
    world_info = request(url)
    return world_info["worlds"]["world"]


# # # # # # # Worlds end # # # # # # #


# # # # # # # Experience # # # # # # #


def get_highscores(
    world, category, profession, site_num
):
    url = f"https://api.tibiadata.com/{api_version}/highscores/{world}/{category}/{profession}/{site_num}"
    highscores = request(url)
    return highscores["highscores"]


# # # # # # # Experience end # # # # # # #


# # # # # # # Character # # # # # # #


def get_character_info(character):
    url = f"https://api.tibiadata.com/{api_version}/character/{character}"
    character = request(url)
    return character["characters"]


# # # # # # # Character end # # # # # # #


def get_kill_statistics(world):
    url = f"https://api.tibiadata.com/{api_version}/killstatistics/{world}"
    kill_statistics = request(url)
    return kill_statistics["killstatistics"]["entries"]