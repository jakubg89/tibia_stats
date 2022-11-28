import requests
import pandas as pd


def scrap_proxy():
    url = 'https://free-proxy-list.net/'
    request = requests.get(url)

    # future check if website is reachable
    # if request.status_code == 200:

    proxy_df = pd.DataFrame(data=pd.read_html(request.text)[0])
    proxy_df = proxy_df[proxy_df['Anonymity'] == 'elite proxy']
    proxy_df = proxy_df[['IP Address', 'Port']].reset_index(drop=True).drop_duplicates(subset='IP Address')
    return proxy_df









