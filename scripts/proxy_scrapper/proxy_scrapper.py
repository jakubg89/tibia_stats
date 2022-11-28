import requests
import pandas as pd


def scrap_proxy():
    url = 'https://free-proxy-list.net/'
    request = requests.get(url)

    if request.status_code == 200:
        proxy_df = pd.DataFrame(data=pd.read_html(request.text)[0])
        proxy_df = proxy_df[proxy_df['Anonymity'] == 'elite proxy']
        proxy_df = proxy_df[['IP Address', 'Port']].reset_index(drop=True).drop_duplicates(subset='IP Address')
        proxy_df.to_csv('proxy_list.csv',
                        encoding='utf-8',
                        index=False,
                        sep=':',
                        header=False,
                        mode='a')


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
