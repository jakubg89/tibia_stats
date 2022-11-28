import pandas as pd
from proxy_scrapper import scrap_proxy


def delete_duplicates():
    try:
        proxy_list = pd.read_csv('proxy_list.csv', sep=':')
        proxy_list = proxy_list.drop_duplicates()
        proxy_list.to_csv('proxy_list.csv',
                          encoding='utf-8',
                          index=False,
                          sep=':',
                          header=False,
                          mode='w')
    except FileNotFoundError:
        scrap_proxy()
        delete_duplicates()


def get_proxy_list():
    temp_list = []
    with open('proxy_list.csv') as file:
        for line in file:
            line = line.strip()
            temp_list.append(line)
    file.close()
    temp_list.pop()
    return temp_list
