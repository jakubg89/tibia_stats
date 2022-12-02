import requests
import random
from bs4 import BeautifulSoup
from time import sleep
import data
import headers
import time
# from scripts.proxy_scrapper.proxy_functions import get_proxy_list
import worlds


class ScrapHighscores:
    def __init__(self):
        category = data.category()
        self.request_headers = headers.headers()
        # self.proxy_list = get_proxy_list()

        self.how_many_sites = 0
        self.file_name = time.strftime('%d_%m_%Y', time.localtime())
        self.path = 'temp/{file_name}.txt'.format(file_name=self.file_name)
        self.column_count = 1
        self.block_first_row = 1
        self.text = ''

        self.access_count_sites = True
        self.access_scrap_sub_site = True
        # self.proxy_num = 0

        for world in worlds.world():
            # print(world, ' ', end='')
            sleep(round(random.randint(5, 20)))
            for prof in data.profession():
                self.url = 'https://www.tibia.com/community/?subtopic=highscores&' \
                            'world={world}&' \
                            'beprotection=-1&' \
                            'category={category}&' \
                            'profession={prof}&' \
                            'currentpage=1'.format(world=world,
                                                   category=category,
                                                   prof=prof,
                                                   verify=True)
                # print(prof, end='')
                self.check = self.count_sites() + 1
                for site_num in range(1, self.check):
                    self.url2 = 'https://www.tibia.com/community/?subtopic=highscores&' \
                                'world={world}&' \
                                'beprotection=-1&' \
                                'category={category}&' \
                                'profession={prof}&' \
                                'currentpage={site_num}'.format(world=world,
                                                                category=category,
                                                                prof=prof,
                                                                site_num=site_num,
                                                                verify=True)
                    # print(self.request.status_code)
                    self.access_scrap_sub_site = True
                    while self.access_scrap_sub_site:
                        # self.proxies = {
                        #    "http": self.proxy_list[self.proxy_num]
                        # }
                        self.request = requests.get(self.url2,
                                                    headers=self.request_headers,
                                                    # proxies=self.proxies,
                                                    verify=True)
                        self.soup = BeautifulSoup(self.request.text, 'html.parser')

                        if self.request.status_code == 403:
                            self.access_scrap_sub_site = True
                            sleep(round(random.uniform(10, 20), 3))

                            # self.proxy_num += 1
                            # print(self.proxy_num)
                            # if self.proxy_num == len(self.proxy_list):
                            #    self.proxy_num = 0
                        else:
                            self.scrap_sub_site()

                            sleep(round(random.uniform(0.8, 2), 3))
                            # print(str(site_num) + '/' + str(self.check) + '-', end='')
                            # print('ok ', end='')
                            # self.proxy_num += 1
                            # if self.proxy_num >= len(self.proxy_list):
                            #     self.proxy_num = 0
                            # print(self.proxy_list[self.proxy_num], self.proxy_num, len(self.proxy_list))
                            self.access_scrap_sub_site = False
                # print()
                self.check = 0

    def count_sites(self):
        # self.how_many_sites = 0
        self.access_count_sites = True
        while self.access_count_sites:
            # self.proxies = {
            #    "http": self.proxy_list[self.proxy_num]
            # }
            self.request = requests.get(self.url,
                                        headers=self.request_headers,
                                        # proxies=self.proxies)
                                        )
            self.soup = BeautifulSoup(self.request.text, 'html.parser')

            if self.request.status_code == 403:
                self.access_count_sites = True
                sleep(round(random.uniform(10, 20), 3))
                # self.proxy_num += 1
                # print(self.proxy_num, end='')
                # if self.proxy_num > len(self.proxy_list):
                #    self.proxy_num = 0
            else:
                # print('ok')
                self.access_count_sites = False
                for self.i in self.soup.findAll('span', {'class': 'PageLink'}):
                    self.how_many_sites += 1
                self.how_many_sites = int(self.how_many_sites / 2)
                return self.how_many_sites
        return self.how_many_sites

    def scrap_sub_site(self):
        for div in self.soup.findAll('div', {'class': 'TableContentContainer'}):
            self.text = ''
            self.block_first_row = 1
            for i in div.findAll('td'):
                # If id is set to Auto Increment
                if self.column_count == 1:
                    self.text = 'NULL'

                # End of row
                elif self.column_count == 6:
                    self.column_count = 0
                    self.text = self.text + ',"'
                    self.text = self.text + i.text.replace(',', '') + '"'
                    self.text = self.text + '\n'

                    # Saving to file
                    if self.block_first_row != 1:
                        self.savefile(self.text)
                    self.block_first_row += 1
                else:
                    self.text = self.text + ',"'
                    self.text = self.text + i.text + '"'
                self.column_count += 1

    def savefile(self, text):
        with open(self.path, 'a', encoding='utf-8') as self.file:
            self.file.write(text)
        self.file.close()
