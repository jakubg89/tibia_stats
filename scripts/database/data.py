# django
from tibia_stats.wsgi import *
from django.db import connection
from django.db.models import Q
from main.models import World, Vocation, Character, Highscores
# from os import environ

# custom
import scripts.tibiadata_API.get_data as dataapi

# other
import os
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
import json
from pathlib import Path


# environ.setdefault('DJANGO_SETTINGS_MODULE', 'tibia_stats.settings')


def main():
    add_boss_to_db()
    add_creature_to_db()
    add_world_online_history()
    add_news_to_db()
    add_news_ticker_to_db()


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
            images_in_news[i][
                'style'] = f"width: {images_in_news[i]['width']}px; height: {images_in_news[i]['height']}px;"
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
                query = f"SELECT EXISTS" \
                        f"(SELECT id_on_tibiacom FROM news WHERE id_on_tibiacom = {i} AND (type='ticker')) as truth;"
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
                        f"INSERT INTO News "
                        f"(news_id, id_on_tibiacom, url_tibiacom, type, content, content_html, date_added) "
                        f"VALUES (NULL,"
                        f" {single_news['id']}, "
                        f"'{single_news['url']}', "
                        f"'{single_news['type']}', "
                        f"'{content}', "
                        f"'{content_html}', "
                        f"'{date}');"
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
    with connection.cursor() as cursor:
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
                    f"SELECT EXISTS(SELECT id_on_tibiacom FROM news "
                    f"WHERE id_on_tibiacom = {i} AND (type='news')) as truth;"
                )
                exist = cursor.fetchone()

                # check the result and perform insert if its not in database
                if exist[0] != 1:
                    single_news = dataapi.get_specific_news(i)

                    # prepare data
                    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    content = add_backslashes(single_news['content'])
                    content_html = add_backslashes(single_news['content_html'])
                    formatted_content = add_backslashes(format_content(content_html))
                    title = add_backslashes(single_news['title'])

                    # execute query
                    cursor.execute(
                        f"INSERT INTO News "
                        f"(news_id, id_on_tibiacom, url_tibiacom, type, content, content_html, date_added, news_title) "
                        f"VALUES (NULL, "
                        f"{single_news['id']}, "
                        f"'{single_news['url']}', "
                        f"'news', "
                        f"'{content}', "
                        f"'{formatted_content}', "
                        f"'{date}', "
                        f"'{title}');"
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
    with connection.cursor() as cursor:
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
                f"INSERT INTO Boosted (boosted_id, name, image_url, type, date_time) "
                f"VALUES (NULL, '{boss_info['name']}', '{boss_info['image_url']}', '{category}', '{date}');"
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
                f"INSERT INTO Boosted (boosted_id, name, image_url, type, date_time) "
                f"VALUES (NULL, '{creature_info['name']}', '{creature_info['image_url']}', '{category}', '{date}');"
            )


# # # # # # # Boosted creature/boss end # # # # # # #


# # # # # # # Worlds # # # # # # #

def add_worlds_information_to_db():
    worlds_information = dataapi.get_worlds_information()
    path_to_json = Path(__file__).resolve().parent.parent
    values = json.load(open(os.path.join(path_to_json, 'tibiacom_scrapper\\temp\\data_value\\data.json')))

    for world in worlds_information:

        # check if list is not empty, if yes we just skip that part. All news tickers are up-to-date.
        if world:
            with connection.cursor() as cursor:

                # check if database already has that id return 1 or 0
                cursor.execute(
                    f"SELECT EXISTS (SELECT name FROM world WHERE name = '{world['name']}') as truth;"
                )
                exist = cursor.fetchone()

                # check the result and perform insert if it's not in database
                if exist[0] != 1:

                    # getting data of creation date if world is initially protected
                    if world['battleye_date'] == 'release':
                        world_details = dataapi.get_world_details(world['name'])
                        date = world_details['creation_date'] + '-01'
                        battleye_value = values['beprotection']['Initially Protected']
                        creation_date = date
                    elif world['battleye_date'] == '':
                        world_details = dataapi.get_world_details(world['name'])
                        date = world_details['creation_date'] + '-01'
                        battleye_value = values['beprotection']['Unprotected']
                        creation_date = date
                    else:
                        world_details = dataapi.get_world_details(world['name'])
                        date = world['battleye_date']
                        battleye_value = values['beprotection']['Protected']
                        creation_date = world_details['creation_date'] + '-01'

                    # add value based on location
                    if world['location'] == 'Europe':
                        location_value = 0
                    elif world['location'] == 'South America':
                        location_value = 1
                    else:
                        location_value = 2

                    # execute query
                    cursor.execute(
                        f"INSERT INTO world (world_id, name, name_value, pvp_type, pvp_type_value, battleye_protected, battleye_date, battleye_value, location, location_value, creation_date) VALUES (NULL, "
                        f"'{world['name']}', "                          # name
                        f"'{values['world'][world['name']]}', "         # name_value
                        f"'{world['pvp_type']}', "                      # pvp_type
                        f"'{values['pvp_type'][world['pvp_type']]}', "  # pvp_value
                        f"'{world['battleye_protected']}', "            # battleye_protected
                        f"'{date}',"                                    # battleye_date
                        f"'{battleye_value}',"                          # battleye_value
                        f"'{world['location']}',"                       # location
                        f"'{location_value}',"                          # location_value
                        f"'{creation_date}');"                          # creation_date
                    )


def add_world_online_history():
    worlds_information_api = dataapi.get_worlds_information()
    worlds_id = {}

    with connection.cursor() as cursor:
        # check if database already has that id return 1 or 0
        cursor.execute(
            f"SELECT name, world_id FROM world;"
        )
        query_result = cursor.fetchall()

        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for i in query_result:
            worlds_id.update({i[0]: i[1]})

        for world in worlds_information_api:

            # execute query
            cursor.execute(
                f"INSERT INTO world_online_history () VALUES (NULL, "
                f"'{worlds_id[world['name']]}', "  # world id
                f"'{world['players_online']}', "  # online players
                f"'{date}');"  # date_time
            )


def add_online_players():
    pass

# # # # # # # Worlds end # # # # # # #


# # # # # # # Experience # # # # # # #

def get_highscores():

    # charms / expierience will be modified to be more elastic
    category = 'experience'

    # proffesions names - all proffesions
    proffesions = [
        'none',
        'knights',
        'paladins',
        'sorcerers',
        'druids'
    ]

    # getting wolrd list ( name = value , for now )
    world_list_from_db = World.objects.all().values('name_value')
    world_list_df = pd.DataFrame(data=world_list_from_db)
    worlds = world_list_df['name_value'].tolist()

    # empty df assignment
    result_df = pd.DataFrame

    # for loop for each world
    for world in worlds:

        # for loop for each profession
        for prof in proffesions:

            # get total site number before executin loop over each site
            # 1-20 sites are possible
            request_from_api = dataapi.get_highscores(world, category, prof, 1)
            site_num = request_from_api['highscore_page']['total_pages']

            # check if there is more than 20 sites
            if site_num >= 20:
                site_num = 20

            # perform collecting data from api for each vocation
            for i in range(1, site_num + 1):
                request_from_api = dataapi.get_highscores(world, category, prof, i)
                if i == 1 and world == worlds[0] and prof == proffesions[0]:
                    result_df = pd.DataFrame(data=request_from_api['highscore_list'])
                else:
                    tempdf = pd.DataFrame(data=request_from_api['highscore_list'])
                    result_df = pd.concat([result_df, tempdf], ignore_index=True)

    # returning collected data in df
    return result_df


def collect_voc_id():   # collect data about vocation from db
    voc = Vocation.objects.all().values('voc_id', 'name')
    voc_df = pd.DataFrame(data=voc)
    formatted_voc_data = {}
    voc_dict = voc_df.to_dict('records')

    for i in voc_dict:
        formatted_voc_data.update({i['name']: i['voc_id']})

    return formatted_voc_data


def collect_world_id():   # collect data about worlds from db
    world = World.objects.all().values('world_id', 'name')
    world_df = pd.DataFrame(data=world)
    formatted_world_data = {}
    world_dict = world_df.to_dict('records')

    for i in world_dict:
        formatted_world_data.update({i['name']: i['world_id']})

    return formatted_world_data


def collect_char_id():   # collect data about character from db
    characters = Character.objects.all().values('id_char', 'name')
    characters_df = pd.DataFrame(data=characters)
    formatted_characters_data = {}
    characters_dict = characters_df.to_dict('records')

    for i in characters_dict:
        formatted_characters_data.update({i['name']: i['id_char']})

    return formatted_characters_data


def filter_highscores_data():   # filter and prepare data to put inside db

    # collect data
    vocations_id = collect_voc_id()
    worlds_id = collect_world_id()
    chars_id = collect_char_id()
    latest_highscores = get_highscores()

    # ============= filter latest data ===============
    # levels higher than 20 ( 40k + record difference between 10-20 )
    latest_highscores = latest_highscores[latest_highscores['level'] > 20]

    # add char id from db
    latest_highscores['name_id_db'] = latest_highscores['name'].map(chars_id).fillna(0).astype('int64')

    # replace world name with db id
    latest_highscores = latest_highscores['world'].map(worlds_id).fillna(0).astype('int64')

    # replace world name with db id
    latest_highscores = latest_highscores['vocation'].map(vocations_id).fillna(0).astype('int64')

    # collect data about characters that don't exist in db
    # 0 represent names that don't exist

    dont_exist = latest_highscores[latest_highscores['name_id_db'] == 0]

    # delete db index
    # latest_highscores.drop('name_id_db', axis=1, inplace=True)

    # filter only lvl's above 100 and rank lower than 900
    dont_exist_filtered = dont_exist[(dont_exist['level'] > 100) & (dont_exist['rank'] < 900)]
    name_list = dont_exist_filtered['name'].values.tolist()

    # creating lists for different options
    name_change = {}
    deleted_characters = []

    # perform individual check of each character
    for i in name_list:
        char = dataapi.get_character_info(i)
        if char['character']['name'] == '':
            # character is deleted
            deleted_characters.append(i)
        elif 'former_names' in char['character']:
            old_name = char['character']['former_names'][0]
            new_name = char['character']['name']
            name_change.update({old_name: new_name})

    # === INSERT =============== CHAR =========================
    # insert new characters to db
    dont_exist_list = dont_exist['name'].values.tolist()
    name_change_list = []
    for key, value in name_change:
        name_change_list.append(value)
    to_remove = name_change_list + deleted_characters
    to_add = [char for char in dont_exist_list if char not in to_remove]
    new_characters = latest_highscores[latest_highscores['name'].isin(to_add)]
    new_characters_dict = new_characters.to_dict('index')
    obj = []
    for i in new_characters_dict:
        char = Character(
            name=new_characters_dict[i]['name'],
            world_id=new_characters_dict[i]['world_id'],
            voc_id=new_characters_dict[i]['voc_id']
        )
        obj.append(char)
    Character.objects.bulk_create(obj)
    # === END INSERT ===========================================

    # === UPDATE ===============================================
    # update character name after name change

    #  for key, value in x.items():
    # Character.objects.filter(name=key).update(name=value)

    # obj = []
    for key, value in name_change.items():
        # char_to_update =
        Character.objects.filter(name=key).update(name=value)
        # obj.append(char_to_update)
    # Character.objects.bulk_update(obj)

    # collect new id's from db
    chars_id_after_update = collect_char_id()
    latest_highscores['name_id_db'] = latest_highscores['name'].map(chars_id_after_update).fillna(0).astype('int64')
    latest_highscores = latest_highscores[latest_highscores['name_id_db'] != 0]

    # collect data from day before from db from last day
    # old_highscores_query = Highscores.objects.all().values(
    # 'exp_rank',
    # 'id_char',
    # 'voc_id',
    # 'world_id',
    # 'level',
    # 'exp_value',
    # 'charm_rank',
    # 'charm_value'
    # )
    # old_highscores_df = pd.DataFrame(data=old_highscores_query)
    #


    # swap key, value in dictionary
    # id_to_name = {}
    # for key, value in chars_id.items()
    #       id_to_name.update({value: key})

    # change old names for new ones
    # for key, value in name_change.items():
    #     old_highscores_df.loc[old_highscores_df.name == key, 'name'] = value

    # replace id to track characters even after name change
    # old_highscores_df['name'] = old_highscores_df['id_char'].map(id_to_name).fillna(0).astype('int64')

    # merge data - inner_data contains only existing characters in db
    inner_data = old_higscores_df.merge(
        latest_highscores,
        on='name',
        how='inner',
        suffixes=(
            '_old',
            '_latest'
        )
    )


    # calculate experience change
    inner_data['exp_diff'] = (inner_data['value_latest'] - inner_data['exp_value_old']).fillna(0).astype('int64')

    # calculate experience rank change
    inner_data['exp_rank_change'] = (inner_data['rank_latest'] - inner_data['exp_rank_old']).fillna(0).astype('int64')

    # calculate level change
    inner_data['level_change'] = (inner_data['level_latest'] - inner_data['level_old']).fillna(0).astype('int64')

    # delte duplicates
    inner_data = inner_data.drop_duplicates('name')

    # add date
    # inner_data['date'] = date_now

    # catch world transfers
    world_transfers = inner_data[inner_data['world_latest'] != inner_data['world_id_old']]

    # # # # # data ready to insert into db # # # # # #

    # === INSERT =============== WORLD ========================
    # insert all transfers to transfer table
    world_transfers_dict = world_transfers.todict('records')

    # === INSERT =============== DELETED_CHARACTERS ===========
    # insert data to deleted table


    # === INSERT =============== NAME CHANGE ========================
    # insert name changes

    # === INSERT =============== HIGHSCORES =========================
    # insert highscores

# # # # # # # Experience end # # # # # # #


if __name__ == '__main__':
    main()
