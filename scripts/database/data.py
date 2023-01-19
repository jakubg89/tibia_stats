from tibia_stats.wsgi import *
from django.db import connection
from django.db.models import Q
from main.models import (World,
                         Vocation,
                         Character,
                         Highscores,
                         WorldTransfers,
                         NameChange,
                         RecordsHistory,
                         News,
                         Boosted,
                         WorldOnlineHistory)

# custom
import scripts.tibiadata_API.get_data as dataapi

# other
import os
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
import json
from pathlib import Path
import sys

sys.path.append('/django-projects/tibia-stats/')
# environ.setdefault('DJANGO_SETTINGS_MODULE', 'tibia_stats.settings')


def main():
    pass
    # after server save and for check around 13-14 cet
    # add_boss_to_db()
    # add_creature_to_db()

    # will see
    # add_world_online_history()

    # every 12 hours
    # add_news_to_db()

    # every 2 hours
    # add_news_ticker_to_db()

    # once a day (every 24h)
    # filter_highscores_data()
    # get_daily_records()
    # TODO clean highscores table and move only active players to history
    # move_active_players_to_history
    # delete_records_from_highscores
    # add_worlds_information_to_db


def add_backslashes(text):
    text = text.replace("'", "\\'")
    return text


def date_with_seconds():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def date_with_day():
    return datetime.now().strftime("%Y-%m-%d")


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
    # if len(paragraphs_in_news) > 1:
    #    formatted_html.find('p', {'id': (len(paragraphs_in_news) - 1)}).decompose()

    return str(formatted_html)


# # # # # # # News ticker # # # # # # #

# adding news to database if it not exists
def add_news_ticker_to_db():

    # get all tibia.com id from database
    db_news = News.objects.all().values('id_on_tibiacom', 'type')
    db_news_df = pd.DataFrame(data=db_news)
    db_news_df = db_news_df[db_news_df['type'] == 'ticker']

    # get 90 day history from tibia.com (news and article)
    all_ticker = dataapi.get_ticker_history()
    all_ticker_df = pd.DataFrame(data=all_ticker)
    all_ticker_df.rename(columns={'id': 'id_on_tibiacom'}, inplace=True)
    all_ticker_df.drop(columns=['date', 'news', 'category', 'url'], inplace=True)
    not_existing_id = db_news_df.merge(all_ticker_df,
                                       on='id_on_tibiacom',
                                       how='right',
                                       indicator=True).query('_merge == "right_only"')

    id_list = not_existing_id['id_on_tibiacom'].values.tolist()

    # check if list is not empty, if yes we just skip that part. All news tickers are up to date.
    if id_list:
        tickers = []
        for i in id_list:
            single_news = dataapi.get_specific_news(i)

            # prepare data
            date = date_with_seconds()
            content = add_backslashes(single_news['content'])
            content_html = add_backslashes(single_news['content_html'])

            ticker = News(id_on_tibiacom=single_news['id'],
                          url_tibiacom=single_news['url'],
                          type=single_news['type'],
                          content=content,
                          content_html=content_html,
                          date_added=date)
            tickers.append(ticker)
        News.objects.bulk_create(tickers)


# # # # # # # News ticker end # # # # # # #


# # # # # # # News # # # # # # #

# adding news to database if it not exists
def add_news_to_db():

    # get all tibia.com id from database
    db_news = News.objects.all().values('id_on_tibiacom', 'type')
    db_news_df = pd.DataFrame(data=db_news)
    db_news_df = db_news_df[db_news_df['type'] == 'news']
    
    # get 90 day history from tibia.com (news and article)
    all_news = dataapi.get_news_history()
    all_news_df = pd.DataFrame(data=all_news)
    all_news_df = all_news_df[all_news_df['type'] == 'news']
    all_news_df.rename(columns={'id': 'id_on_tibiacom'}, inplace=True)
    all_news_df.drop(columns=['date', 'news', 'category', 'url'], inplace=True)

    not_existing_id = db_news_df.merge(all_news_df,
                                       on='id_on_tibiacom',
                                       how='right',
                                       indicator=True).query('_merge == "right_only"')

    id_list = not_existing_id['id_on_tibiacom'].values.tolist()

    # check if list is not empty, if yes we just skip that part. All news tickers are up to date.
    if id_list:
        obj = []
        for i in id_list:
            single_news = dataapi.get_specific_news(i)

            # prepare data
            date = date_with_seconds()
            content = add_backslashes(single_news['content'])
            content_html = add_backslashes(single_news['content_html'])
            formatted_content = add_backslashes(format_content(content_html))
            title = add_backslashes(single_news['title'])

            news = News(id_on_tibiacom=single_news['id'],
                        url_tibiacom=single_news['url'],
                        type='news',
                        content=content,
                        content_html=formatted_content,
                        date_added=date,
                        news_title=title)
            obj.append(news)
        News.objects.bulk_create(obj)

# # # # # # # News end # # # # # # #


# # # # # # # Boosted creature/boss # # # # # # #

# adds boosted boss to database
def add_boss_to_db():
    boss_info = dataapi.boosted_boss()
    category = 'boss'

    # check if list is not empty
    if boss_info:
        date = date_with_seconds()

        boss = Boosted(name=boss_info['name'],
                       image_url=boss_info['image_url'],
                       type=category,
                       date_time=date)
        boss.save()


# adds boosted creature to database
def add_creature_to_db():
    creature_info = dataapi.boosted_creature()
    category = 'creature'

    # check if list is not empty
    if creature_info:
        date = date_with_seconds()

        creature = Boosted(name=creature_info['name'],
                           image_url=creature_info['image_url'],
                           type=category,
                           date_time=date)
        creature.save()


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

    world_id = World.objects.all().values('name', 'world_id')
    world_id_df = pd.DataFrame(data=world_id)
    worlds_id_dict = world_id_df.set_index('name')['world_id'].to_dict()

    date = date_with_seconds()
    obj = []
    for world in worlds_information_api:
        players_online = WorldOnlineHistory(world_id=worlds_id_dict[world['name']],
                                            players_online=world['players_online'],
                                            date=date)
        obj.append(players_online)
    WorldOnlineHistory.objects.bulk_create(obj)


def add_online_players():
    pass

# # # # # # # Worlds end # # # # # # #


# # # # # # # Experience # # # # # # #

def get_highscores():

    # charms / expierience will be modified to be more elastic
    category = 'experience'

    # proffesions names - all proffesions
    proffesions = ['none',
                   'knights',
                   'paladins',
                   'sorcerers',
                   'druids']

    # getting world list ( name = value , for now )
    world_list_from_db = World.objects.all().values('name_value')
    world_list_df = pd.DataFrame(data=world_list_from_db)
    worlds = world_list_df['name_value'].tolist()

    # empty df assignment
    result_df = pd.DataFrame

    # for loop for each world
    for world in worlds:

        # for loop for each profession
        for prof in proffesions:
            # get total site number before execution loop over each site

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


# collect data about vocation from db
def collect_voc_id():

    voc = Vocation.objects.all().values('voc_id', 'name')
    voc_df = pd.DataFrame(data=voc)
    formatted_voc_data = {}
    voc_dict = voc_df.to_dict('records')

    for i in voc_dict:
        formatted_voc_data.update({i['name']: i['voc_id']})

    return formatted_voc_data


# collect data about worlds from db
def collect_world_id():

    world = World.objects.all().values('world_id', 'name')
    world_df = pd.DataFrame(data=world)
    formatted_world_data = {}
    world_dict = world_df.to_dict('records')

    for i in world_dict:
        formatted_world_data.update({i['name']: i['world_id']})

    return formatted_world_data


# collect data about character from db
def collect_char_id():

    characters = Character.objects.all().values('id_char', 'name')
    characters_df = pd.DataFrame(data=characters)
    formatted_characters_data = {}
    characters_dict = characters_df.to_dict('records')

    for i in characters_dict:
        formatted_characters_data.update({i['name']: i['id_char']})

    return formatted_characters_data


# filter and prepare data to put inside db
def filter_highscores_data():

    # collect data
    date = date_with_seconds()

    vocations_id = collect_voc_id()
    worlds_id = collect_world_id()
    chars_id = collect_char_id()

    latest_highscores = get_highscores()
    # for development read from file
    # latest_highscores = pd.read_json
    # ('G:\\Python nauka\\django\\strony\\tibia_stats\\ignore\\pandas\\21test1.txt', orient='columns')

    # ============= filter latest data ===============

    # levels higher than 20 ( 40k + record difference between 10-20 )
    latest_highscores = latest_highscores[latest_highscores['level'] > 20]

    # add char id from db
    latest_highscores['name_id_db'] = latest_highscores['name'].map(chars_id).fillna(0).astype('int64')

    # replace world name with db id
    latest_highscores['world'] = latest_highscores['world'].map(worlds_id).fillna(0).astype('int64')

    # replace world name with db id
    latest_highscores['vocation'] = latest_highscores['vocation'].map(vocations_id).fillna(0).astype('int64')

    # collect data about characters that don't exist in db
    # 0 represent names that don't exist
    dont_exist = latest_highscores[latest_highscores['name_id_db'] == 0]

    # delete db index
    latest_highscores.drop('name_id_db', axis=1, inplace=True)

    # perform individual check of each character
    name_change = {}
    deleted_characters = []
    new_names = []
    name_list_dont_exist = dont_exist['name'].values.tolist()

    for i in name_list_dont_exist:
        char = dataapi.get_character_info(i)
        if char['character']['name'] == '':
            # character is deleted
            deleted_characters.append(i)
        elif 'former_names' in char['character']:
            old_name = char['character']['former_names'][0]
            new_name = char['character']['name']
            name_change.update({old_name: new_name})
            new_names.append(new_name)

    #
    # === INSERT =============== CHARACTER ===================

    # insert new characters to db

    name_list = set(name_list_dont_exist).difference(new_names)
    if name_list:
        new_characters = latest_highscores[latest_highscores['name'].isin(name_list)]
        new_characters_dict = new_characters.to_dict('index')
        obj = []
        for i in new_characters_dict:
            char = Character(name=new_characters_dict[i]['name'],
                             world_id=new_characters_dict[i]['world'],
                             voc_id=new_characters_dict[i]['vocation']
                             )
            obj.append(char)
        Character.objects.bulk_create(obj)

    # === END INSERT ===========================================
    #

    #
    # === UPDATE ================ CHARACTER ====================
    # update character name after name change

    if name_change:
        obj = []

        for key, value in name_change.items():
            char_to_update = Character.objects.filter(name=key).update(name=value)
            obj.append(char_to_update)

    # === END UPDATE ============================================
    #

    # collect new id's from db
    chars_id_after_update = collect_char_id()
    latest_highscores['name_id_db'] = latest_highscores['name'].map(chars_id_after_update).fillna(0).astype('int64')
    latest_highscores = latest_highscores[latest_highscores['name_id_db'] != 0]

    # collect data from day before from db from last day
    old_highscores_query = Highscores.objects.all().filter(Q(date__gt='2022-12-23 11:12:49')).values('exp_rank',
                                                                                                     'id_char',
                                                                                                     'voc_id',
                                                                                                     'world_id',
                                                                                                     'level',
                                                                                                     'exp_value',
                                                                                                     'charm_rank',
                                                                                                     'charm_value')

    old_highscores_df = pd.DataFrame(data=old_highscores_query)

    # swap key(name), value(id_char) in dictionary
    id_to_name = {}
    for key, value in chars_id_after_update.items():
        id_to_name.update({value: key})

    old_highscores_df['name'] = old_highscores_df['id_char'].map(id_to_name)

    # change old names for new ones
    for key, value in name_change.items():
        old_highscores_df.loc[old_highscores_df.name == key, 'name'] = value

    # merge data - inner_data contains only existing characters in db
    inner_data = old_highscores_df.merge(latest_highscores,
                                         on='name',
                                         how='inner',
                                         suffixes=('_old',
                                                   '_latest'))

    # calculate experience change
    inner_data['exp_diff'] = (inner_data['value'] - inner_data['exp_value']).fillna(0).astype('int64')

    # calculate experience rank change
    inner_data['exp_rank_change'] = (inner_data['exp_rank'] - inner_data['rank']).fillna(0).astype('int64')

    # calculate level change
    inner_data['level_change'] = (inner_data['level_latest'] - inner_data['level_old']).fillna(0).astype('int64')

    # delete duplicates
    inner_data = inner_data.drop_duplicates('name')

    # catch world transfers
    world_transfers = inner_data[inner_data['world_id'] != inner_data['world']]

    #
    # === INSERT =============== WORLD ========================
    # insert all transfers to transfer table

    id_to_world = {}
    for key, value in worlds_id.items():
        id_to_world.update({value: key})

    obj_world = []
    traded = 0      # temp variable
    world_transfers_dict = world_transfers.to_dict('index')
    for i in world_transfers_dict:
        transfer = WorldTransfers(id_char_id=world_transfers_dict[i]['id_char'],
                                  old_world=id_to_world[world_transfers_dict[i]['world_id']],
                                  oldid=world_transfers_dict[i]['world_id'],
                                  new_world=id_to_world[world_transfers_dict[i]['world']],
                                  newid=world_transfers_dict[i]['world'],
                                  level=world_transfers_dict[i]['level_latest'],
                                  traded=traded,
                                  date=date)
        obj_world.append(transfer)
    WorldTransfers.objects.bulk_create(obj_world)

    # === END INSERT =============== WORLD ====================
    #

    #
    # === INSERT =============== DELETED_CHARACTERS ===========

    # insert data to deleted table - for future
    # future develop
    # print(deleted_characters)
    # deleted_df = inner_data[inner_data['name'].isin(deleted_characters)]
    # print('deleted df')
    # print()
    # print(deleted_df)
    # Columns: [exp_rank, id_char, voc_id, world_id, level_old, exp_value, charm_rank, charm_value,
    # name, rank, vocation, world, level_latest, value, name_id_db, exp_diff, exp_rank_change, level_change]
    # deleted_dict = deleted_df.to_dict('index')

    # for do bulk
    #
    # === END INSERT ========= DELETED_CHARACTERS ==============
    #

    #
    # === INSERT =============== NAME CHANGE ====================

    # insert name changes
    if name_change:

        name_change_list = []
        for key, value in name_change.items():
            name_change_list.append(value)

        names_df = pd.DataFrame({'old_name': list(name_change.keys()),
                                 'name': list(name_change.values())})
        name_change_df = latest_highscores[latest_highscores['name'].isin(name_change_list)]

        name_changes = name_change_df.merge(names_df,
                                            on='name',
                                            how='inner',
                                            suffixes=('_old',
                                                      '_latest'))

        obj_name_change = []
        traded = 0  # temp variable
        name_change_dict = name_changes.to_dict('index')
        for i in name_change_dict:
            xxx = NameChange(id_char_id=name_change_dict[i]['name_id_db'],
                             old_name=name_change_dict[i]['old_name'],
                             new_name=name_change_dict[i]['name'],
                             level=name_change_dict[i]['level'],
                             traded=traded,
                             date=date)
            obj_name_change.append(xxx)
        NameChange.objects.bulk_create(obj_name_change)

    # === END INSERT =============== NAME CHANGE =================
    #

    #
    # === INSERT =============== HIGHSCORES ======================

    # insert highscores

    charm = 0   # temp variable
    obj = []
    inner_data_dict = inner_data.to_dict('index')
    for i in inner_data_dict:
        char = Highscores(exp_rank=inner_data_dict[i]['rank'],
                          exp_rank_change=inner_data_dict[i]['exp_rank_change'],
                          id_char_id=inner_data_dict[i]['id_char'],
                          voc_id=inner_data_dict[i]['vocation'],
                          world_id=inner_data_dict[i]['world'],
                          level=inner_data_dict[i]['level_latest'],
                          level_change=inner_data_dict[i]['level_change'],
                          exp_value=inner_data_dict[i]['value'],
                          exp_diff=inner_data_dict[i]['exp_diff'],
                          charm_rank=charm,
                          charm_rank_change=charm,
                          charm_value=charm,
                          charm_diff=charm,
                          date=date)
        obj.append(char)
    Highscores.objects.bulk_create(obj, 1000)

    #
    # === END INSERT =============== HIGHSCORES ==================


def get_daily_records():
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 2000)

    # best exp yesterday on each world
    # now = datetime.datetime.now()
    # date = (now - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    date = '2023-01-01 11:11:50'

    # world_types = {
    #    0: 'Open PvP',
    #    1: 'Optional PvP',
    #    3: 'Retro Open PvP',
    #    4: 'Retro Hardcore PvP'
    # }

    # getting world list id
    world_list_from_db = World.objects.all().values('world_id')
    world_list_df = pd.DataFrame(data=world_list_from_db)
    worlds = world_list_df['world_id'].tolist()

    # getting vocation list id
    vocation_list_from_db = Vocation.objects.all().values('voc_id')
    vocation_list_df = pd.DataFrame(data=vocation_list_from_db)
    vocations = vocation_list_df['voc_id'].tolist()

    # getting the best exp (each vocation on every world)
    best = Highscores.objects.filter(Q(date__gt=date)
                                     & Q(exp_diff__gt=0)
                                     | Q(exp_diff__lt=0)).values('exp_rank',
                                                                 'exp_rank_change',
                                                                 'id_char',
                                                                 'voc_id',
                                                                 'world_id',
                                                                 'level',
                                                                 'level_change',
                                                                 'exp_value',
                                                                 'exp_diff',
                                                                 'charm_rank',
                                                                 'charm_rank_change',
                                                                 'charm_value',
                                                                 'charm_diff',
                                                                 'date')
    db_data_to_df = pd.DataFrame(data=best)

    # best_df[best_df['world_id'] == 1].sort_values(by='exp_diff').tail(1)

    # best experience gained
    for world in worlds:
        for vocation in vocations:

            worst_exp = db_data_to_df[(db_data_to_df['world_id'] == world)
                                      & (db_data_to_df['voc_id'] == vocation)].sort_values(by='exp_diff').tail(1)

            if world == 1 and vocation == 1:
                history = worst_exp
            else:
                history = pandas.concat([worst_exp, history], ignore_index=True)

    # biggest lost experience
    for world in worlds:
        for vocation in vocations:

            worst_exp = db_data_to_df[(db_data_to_df['world_id'] == world)
                                      & (db_data_to_df['voc_id'] == vocation)
                                      & (db_data_to_df['exp_diff'] < 0)].sort_values(by='exp_diff').head(1)

            history = pandas.concat([worst_exp, history], ignore_index=True)

    charm = 0
    record_type = 'exp'
    event = 'none'
    obj = []
    history_dict = history.to_dict('index')
    for i in history_dict:
        record = RecordsHistory(exp_rank=history_dict[i]['exp_rank'],
                                exp_rank_change=history_dict[i]['exp_rank_change'],
                                id_char_id=history_dict[i]['id_char'],
                                voc_id=history_dict[i]['voc_id'],
                                world_id=history_dict[i]['world_id'],
                                level=history_dict[i]['level'],
                                level_change=history_dict[i]['level_change'],
                                exp_value=history_dict[i]['exp_value'],
                                exp_diff=history_dict[i]['exp_diff'],
                                charm_rank=charm,
                                charm_rank_change=charm,
                                charm_value=charm,
                                charm_diff=charm,
                                record_type=record_type,
                                event=event,
                                date=date)
        obj.append(record)
    RecordsHistory.objects.bulk_create(obj)


# # # # # # # Experience end # # # # # # #


if __name__ == '__main__':
    main()
