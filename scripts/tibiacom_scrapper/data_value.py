import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
import os


def get_data_category_values():
    base_dir = Path(__file__).resolve().parent.parent
    path = os.path.join(base_dir, 'tibiacom_scrapper\\temp\\data_value\\data.json')
    data_categories = [
        'world',
        'beprotection',
        'category',
        'profession'
    ]

    url = 'https://www.tibia.com/community/?subtopic=highscores'
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')

    name_and_value = {}
    for item in data_categories:
        data = {}
        for option in soup.find_all('select', {'name': item}):
            for i in option.findAll('option'):
                if i['value'] != '':
                    data.update({i.text: i['value']})
        name_and_value.update({item: data})

    with open(path, 'w') as file:
        json.dump(name_and_value, file)
