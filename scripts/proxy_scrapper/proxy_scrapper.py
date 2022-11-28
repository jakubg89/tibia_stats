import requests
from bs4 import BeautifulSoup
import pandas as pd
import os


def scrap_proxy():
    url = 'https://free-proxy-list.net/'
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')

    # future check if website is reachable
    # if request.status_code == 200:

    tables = soup.find('table', {'class': 'table table-striped table-bordered'})
    data = pd.DataFrame(columns=['ip',
                                 'port',
                                 'code',
                                 'country',
                                 'anonymity',
                                 'google',
                                 'https',
                                 'last checked'])

    for row in tables.findAll('tr'):
        # Find all data for each column
        columns = row.find_all('td')
        if columns:
            ip = columns[0].text.strip()
            port = columns[1].text.strip()
            code = columns[2].text.strip()
            country = columns[3].text.strip()
            anonymity = columns[4].text.strip()
            google = columns[5].text.strip()
            https = columns[6].text.strip()
            last_checked = columns[7].text.strip()

            data2 = {'ip': ip,
                     'port': port,
                     'code': code,
                     'country': country,
                     'anonymity': anonymity,
                     'google': google,
                     'https': https,
                     'last checked': last_checked}
            data3 = pd.DataFrame(data=data2, index=[0])

            data = pd.concat([data, data3], ignore_index=True)

    return data

x = scrap_proxy()

print(x)
test = x[['ip', 'port', 'anonymity']]
# print(test)

sprawdzam = test[test['anonymity'] == 'elite proxy']
sprawdzam = sprawdzam[['ip', 'port']]
sprawdzam = sprawdzam.drop_duplicates(subset='ip')
sprawdzam = sprawdzam.reset_index(drop=True)
# sprawdzam = sprawdzam.reindex()
# print((sprawdzam[['ip', 'port']].to_string(index=False)).strip())
mojalista = sprawdzam.to_dict()

mojslownik = sprawdzam.set_index('ip')['port'].to_dict()
#print(sprawdzam.to_string(index=True))

#print(mojalista)
#print(mojslownik)

listaproxy = []
for key, value in mojslownik.items():
    x = key+':'+value
    listaproxy.append(x)

for i in listaproxy:
    print(i)



