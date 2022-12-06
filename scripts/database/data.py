from django.db import connection
from os import environ
import pandas as pd
import scripts.tibiadata_API.get_data as dataapi
from datetime import datetime
from bs4 import BeautifulSoup

environ.setdefault('DJANGO_SETTINGS_MODULE', 'tibia_stats.settings')


def add_backslashes(text):
    text = text.replace("'", "\\'")
    return text


def format_content(raw_html):
    formatted_html = BeautifulSoup(raw_html, 'html.parser')

    # finds all images in news and adds style, class and onclick action
    images_in_news = formatted_html.find_all('img')
    for i in range(len(images_in_news)):
        images_in_news[i]['onclick'] = ''

        # check if there are all attributes
        try:
            images_in_news[i]['style'] = f"width: {images_in_news[i]['width']}px; height: {images_in_news[i]['height']}px;"
        except KeyError as x:
            if x == 'height':
                images_in_news[i]['style'] = f"width: {images_in_news[i]['width']}px;"
            elif x == 'width':
                images_in_news[i]['style'] = f"height: {images_in_news[i]['height']}px;"

    # finds all paragraphs in news and adds id
    paragraphs_in_news = formatted_html.find_all('p')
    for i in range(len(paragraphs_in_news)):
        paragraphs_in_news[i]['id'] = i

    # deleting last paragraph
    if len(paragraphs_in_news) > 1:
        formatted_html.find('p', {'id': (len(paragraphs_in_news) - 1)}).decompose()
    return str(formatted_html)


# # # # # # # News ticker # # # # # # #

# adding news to database if it not exists
def add_news_ticker_to_db():

    # get latest id list
    id_list = get_latest_news_ticker_id()

    # check if list is not empty, if yes we just skip that part. All news tickers are up to date.
    if id_list:
        for i in id_list:
            with connection.cursor() as cursor:

                # check if database already has that id return 1 or 0
                query = "SELECT EXISTS(SELECT id_on_tibiacom FROM news WHERE id_on_tibiacom = {id} AND (type='ticker')) as truth;" \
                    .format(id=i)
                cursor.execute(query)
                exist = cursor.fetchone()

                # check the result and perform insert if its not in database
                if exist[0] != 1:
                    single_news = dataapi.get_specific_news(i)

                    # prepare data
                    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    content = add_backslashes(single_news['content'])
                    content_html = add_backslashes(single_news['content_html'])

                    # execute query
                    cursor.execute(
                        "INSERT INTO News (news_id,"
                        " id_on_tibiacom, url_tibiacom, type, content, content_html, date_added)"
                        " VALUES (NULL, {id}, '{url}', '{type}', '{content}', '{content_html}', '{date}');"
                        .format(
                            id=single_news['id'],
                            url=single_news['url'],
                            type=single_news['type'],
                            content=content,
                            content_html=content_html,
                            date=date
                        )
                    )


# compare list of latest 90 days history of news from tibia.com to existing ones in database
def get_latest_news_ticker_id():
    # getting dictionary from tibia.com with all news from last 90 days
    all_tickers = dataapi.get_ticker_history()
    all_id_tibia_com = []
    all_id_db = []

    # assign id to list
    for row in all_tickers:
        all_id_tibia_com.append(row['id'])

    # getting list of id from db which are not older than 90 days
    with connection.cursor()as cursor:
        cursor.execute(
            'SELECT id_on_tibiacom FROM news WHERE date_added >= (NOW() - INTERVAL 90 DAY) AND (type="ticker");'
        )
        query_result = cursor.fetchall()
    for row in query_result:
        all_id_db.append(row[0])

    # return list of unique id that are not included in db
    return list(set(all_id_tibia_com) - set(all_id_db))

# # # # # # # News ticker end # # # # # # #


# # # # # # # News # # # # # # #

# adding news to database if it not exists
def add_news_to_db():

    # get latest id list
    id_list = get_latest_news_id()

    # check if list is not empty, if yes we just skip that part. All news tickers are up to date.
    if id_list:
        for i in id_list:
            with connection.cursor() as cursor:

                # check if database already has that id return 1 or 0
                cursor.execute(
                    "SELECT EXISTS(SELECT id_on_tibiacom FROM news "
                    "WHERE id_on_tibiacom = {id} AND (type='news')) as truth;"
                    .format(
                        id=i
                    )
                )
                exist = cursor.fetchone()

                # check the result and perform insert if its not in database
                if exist[0] != 1:
                    single_news = dataapi.get_specific_news(i)

                    # prepare data
                    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    content = add_backslashes(single_news['content'])
                    content_html = add_backslashes(single_news['content_html'])
                    formatted_content = format_content(content_html)
                    title = add_backslashes(single_news['title'])

                    # execute query
                    cursor.execute(
                        "INSERT INTO News (news_id,"
                        " id_on_tibiacom, url_tibiacom, type, content, content_html, date_added, title)"
                        " VALUES (NULL, {id}, '{url}', '{type}', '{content}', '{content_html}', '{date}', '{title}');"
                        .format(
                            id=single_news['id'],
                            url=single_news['url'],
                            type='news',
                            content=content,
                            content_html=formatted_content,
                            date=date,
                            title=title,
                        )
                    )


def get_latest_news_id():
    # getting dictionary from tibia.com with all news from last 90 days
    all_news = dataapi.get_news_history()
    all_id_tibia_com = []
    all_id_db = []

    # assign id to list
    for row in all_news:
        all_id_tibia_com.append(row['id'])

    # getting list of id from db which are not older than 90 days
    with connection.cursor()as cursor:
        cursor.execute(
            'SELECT id_on_tibiacom FROM news WHERE date_added >= (NOW() - INTERVAL 90 DAY) AND (type="news");'
        )
        query_result = cursor.fetchall()
    for row in query_result:
        all_id_db.append(row[0])

    # return list of unique id that are not included in db
    return list(set(all_id_tibia_com) - set(all_id_db))

# # # # # # # News end # # # # # # #


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
            cursor.execute(
                "INSERT INTO Boosted (boosted_id,"
                " name, image_url, type, date)"
                " VALUES (NULL, '{name}', '{image_url}', '{type}', '{date}');"
                .format(
                    name=boss_info['name'],
                    image_url=boss_info['image_url'],
                    type=category,
                    date=date
                )
            )


# adds boosted creature to database
def add_creature_to_db():
    creature_info = dataapi.boosted_creature()
    category = 'creature'

    # check if list is not empty
    if creature_info:
        date = datetime.now().strftime("%Y-%m-%d")
        with connection.cursor() as cursor:

            # execute query
            cursor.execute(
                "INSERT INTO Boosted (boosted_id,"
                " name, image_url, type, date)"
                " VALUES (NULL, '{name}', '{image_url}', '{type}', '{date}');"
                .format(
                    name=creature_info['name'],
                    image_url=creature_info['image_url'],
                    type=category,
                    date=date
                )
            )

# # # # # # # Boosted creature/boss end # # # # # # #


add_news_to_db()