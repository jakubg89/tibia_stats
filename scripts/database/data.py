from django.db import connection
from os import environ
import pandas as pd
import scripts.tibiadata_API.get_data as dataapi
from datetime import datetime

environ.setdefault('DJANGO_SETTINGS_MODULE', 'tibia_stats.settings')


def format_data(text):
    text = text.replace("'", "\\'")
    return text


# # # # # # # News ticker # # # # # # #

# adding news to database if it not exists
def add_news_to_db():

    # get latest id list
    id_list = get_latest_news_id()

    # check if list is not empty, if yes we just skip that part. All news tickers are up to date.
    if id_list:
        for i in id_list:
            with connection.cursor() as cursor:

                # check if database already has that id return 1 or 0
                query = "SELECT EXISTS(SELECT id_on_tibiacom FROM news WHERE id_on_tibiacom = {id}) as truth;" \
                    .format(id=i)
                cursor.execute(query)
                exist = cursor.fetchone()

                # check the result and perform insert if its not in database
                if exist[0] != 1:
                    single_news = dataapi.get_specific_news(i)

                    # prepare data
                    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    content = format_data(single_news['content'])
                    content_html = format_data(single_news['content_html'])

                    # execute query
                    cursor.execute("INSERT INTO News (news_id,"
                                   " id_on_tibiacom, url_tibiacom, type, content, content_html, date_added)"
                                   " VALUES (NULL, {id}, '{url}', '{type}', '{content}', '{content_html}', '{date}');"
                                   .format(id=single_news['id'],
                                           url=single_news['url'],
                                           type=single_news['type'],
                                           content=content,
                                           content_html=content_html,
                                           date=date))


# compare list of latest 90 days history of news from tibia.com to existing ones in database
def get_latest_news_id():
    # getting dictionary from tibia.com with all news from last 90 days
    all_tickers = dataapi.get_ticker_history()
    all_id_tibia_com = []
    all_id_db = []

    # assign id to list
    for row in all_tickers:
        all_id_tibia_com.append(row['id'])

    # getting list of id from db which are not older than 90 days
    with connection.cursor()as cursor:
        cursor.execute('SELECT id_on_tibiacom FROM news WHERE date_added >= (NOW() - INTERVAL 90 DAY);')
        query_result = cursor.fetchall()
    for row in query_result:
        all_id_db.append(row[0])

    # return list of unique id that are not included in db
    return list(set(all_id_tibia_com) - set(all_id_db))

# # # # # # # News ticker end # # # # # # #


# # # # # # # Boosted creature/boss # # # # # # #

# adds boosted boss to database
def add_boss_to_db():
    boss_info = dataapi.boosted_boss()
    category = 'boss'

    # check if list is not empty
    if boss_info:
        date = datetime.now().strftime("%Y-%m-%d")
        with connection.cursor() as cursor:

            # execute query
            cursor.execute("INSERT INTO Boosted (boosted_id,"
                           " name, image_url, type, date)"
                           " VALUES (NULL, '{name}', '{image_url}', '{type}', '{date}');"
                           .format(name=boss_info['name'],
                                   image_url=boss_info['image_url'],
                                   type=category,
                                   date=date))


# adds boosted creature to database
def add_creature_to_db():
    creature_info = dataapi.boosted_creature()
    category = 'creature'

    # check if list is not empty
    if creature_info:
        date = datetime.now().strftime("%Y-%m-%d")
        with connection.cursor() as cursor:

            # execute query
            cursor.execute("INSERT INTO Boosted (boosted_id,"
                           " name, image_url, type, date)"
                           " VALUES (NULL, '{name}', '{image_url}', '{type}', '{date}');"
                           .format(name=creature_info['name'],
                                   image_url=creature_info['image_url'],
                                   type=category,
                                   date=date))

# # # # # # # Boosted creature/boss end # # # # # # #


# # # # # # # News # # # # # # #
# # # # # # # News end # # # # # # #


add_creature_to_db()
