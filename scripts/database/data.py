from django.db import connection
from os import environ
import pandas as pd
import scripts.tibiadata_API.get_data as dataapi
from datetime import datetime


environ.setdefault('DJANGO_SETTINGS_MODULE', 'tibia_stats.settings')


# adding news to database if it not exists
def add_news_to_db():

    # get latest id list
    id_list = get_latest_news_id()
    for i in id_list:
        with connection.cursor() as cursor:

            # check if database already has that id return 1 or 0
            query = "SELECT EXISTS(SELECT id_on_tibiacom FROM news WHERE id_on_tibiacom = {id}) as truth;"\
                .format(id=i)
            cursor.execute(query)
            exist = cursor.fetchone()

            # check the result and perform insert if its not in database
            if exist[0] != 1:
                single_news = dataapi.get_specific_news(i)

                # prepare data
                date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                content = single_news['content'].replace("'", "\\'")
                content_html = single_news['content_html'].replace("'", "\\'")

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

add_news_to_db()