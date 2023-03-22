import gc
import sys

sys.path.append("/django-projects/tibia-stats/")
import tibia_stats.settings
from tibia_stats.wsgi import *
from django.db import connection
from django.db.models import Q
from main.models import (
    World,
    Vocation,
    Character,
    Highscores,
    WorldTransfers,
    NameChange,
    RecordsHistory,
    News,
    Boosted,
    WorldOnlineHistory,
    HighscoresHistory,
    Tasks,
    BossStats,
    MonsterStats,
    Monsters,
    Bosses,
)

# custom
import scripts.tibiadata_API.get_data as dataapi

# other
import os
import pandas as pd
from datetime import datetime, timedelta
import datetime
from bs4 import BeautifulSoup
import json
import numpy as np

import logging
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

logging.basicConfig(
    level=logging.INFO,
    # filename="/django-projects/tibia-stats/logs/highscores.log",
    filename=f"{tibia_stats.settings.LOG_DIRECTORY_PATH}highscores.log",
    filemode="a",
)

# All of this is already happening by default!
sentry_logging = LoggingIntegration(
    level=logging.INFO,  # Capture info and above as breadcrumbs
    event_level=logging.ERROR,  # Send errors as events
)

sentry_sdk.init(
    dsn=os.environ.get("DSN"),
    integrations=[
        sentry_logging,
    ],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,
)

# environ.setdefault('DJANGO_SETTINGS_MODULE', 'tibia_stats.settings')


def main():
    pass


def temp_del():
    now = datetime.datetime.now()
    date = "2023-02-01 04:00:00"
    clear_data_query = Highscores.objects.filter(date__gt=date)

    clear_data_query._raw_delete(clear_data_query.db)


def add_backslashes(text):
    text = text.replace("'", "\\'")
    return text


def date_with_seconds():
    return datetime.datetime.now()


def format_content(raw_html):
    formatted_html = BeautifulSoup(raw_html, "html.parser")

    # finds all images in news and adds style, class and onclick action
    images_in_news = formatted_html.find_all("img")
    for i in range(len(images_in_news)):
        images_in_news[i]["onclick"] = ""

        # check if there are all attributes
        try:
            images_in_news[i][
                "style"
            ] = f"width: {images_in_news[i]['width']}px; height: {images_in_news[i]['height']}px;"
        except KeyError as x:
            if x == "height":
                images_in_news[i][
                    "style"
                ] = f"width: {images_in_news[i]['width']}px;"
            elif x == "width":
                images_in_news[i][
                    "style"
                ] = f"height: {images_in_news[i]['height']}px;"

    # finds all paragraphs in news and adds id
    paragraphs_in_news = formatted_html.find_all("p")
    for i in range(len(paragraphs_in_news)):
        paragraphs_in_news[i]["id"] = i

    return str(formatted_html)


# # # # # # # News ticker # # # # # # #


# adding news to database if it not exists
def add_news_ticker_to_db():
    # get all tibia.com id from database
    db_news = News.objects.all().values("id_on_tibiacom", "type")
    db_news_df = pd.DataFrame(data=db_news)
    db_news_df = db_news_df[db_news_df["type"] == "ticker"]

    # get 90 day history from tibia.com (news and article)
    all_ticker = dataapi.get_ticker_history()
    all_ticker_df = pd.DataFrame(data=all_ticker)
    all_ticker_df.rename(columns={"id": "id_on_tibiacom"}, inplace=True)
    all_ticker_df.drop(
        columns=["date", "news", "category", "url"], inplace=True
    )
    not_existing_id = db_news_df.merge(
        all_ticker_df, on="id_on_tibiacom", how="right", indicator=True
    ).query('_merge == "right_only"')

    id_list = not_existing_id["id_on_tibiacom"].values.tolist()

    # check if list is not empty, if yes we just skip that part.
    # All news tickers are up to date.
    if id_list:
        tickers = []
        for i in id_list:
            single_news = dataapi.get_specific_news(i)

            # prepare data
            date = date_with_seconds()
            content = add_backslashes(single_news["content"])
            content_html = add_backslashes(single_news["content_html"])

            ticker = News(
                id_on_tibiacom=single_news["id"],
                url_tibiacom=single_news["url"],
                type=single_news["type"],
                content=content,
                content_html=content_html,
                date_added=date,
            )
            tickers.append(ticker)
        News.objects.bulk_create(tickers)


# # # # # # # News ticker end # # # # # # #


# # # # # # # News # # # # # # #


# adding news to database if it not exists
def add_news_to_db():
    # get all tibia.com id from database
    db_news = News.objects.all().values("id_on_tibiacom", "type")
    db_news_df = pd.DataFrame(data=db_news)
    db_news_df = db_news_df[db_news_df["type"] == "news"]

    # get 90 day history from tibia.com (news and article)
    all_news = dataapi.get_news_history()
    all_news_df = pd.DataFrame(data=all_news)
    all_news_df = all_news_df[all_news_df["type"] == "news"]
    all_news_df.rename(columns={"id": "id_on_tibiacom"}, inplace=True)
    all_news_df.drop(columns=["date", "news", "category", "url"], inplace=True)

    not_existing_id = db_news_df.merge(
        all_news_df, on="id_on_tibiacom", how="right", indicator=True
    ).query('_merge == "right_only"')

    id_list = not_existing_id["id_on_tibiacom"].values.tolist()

    # check if list is not empty, if yes we just skip that part.
    # All news tickers are up to date.
    if id_list:
        obj = []
        for i in id_list:
            single_news = dataapi.get_specific_news(i)

            # prepare data
            date = date_with_seconds()
            content = add_backslashes(single_news["content"])
            content_html = add_backslashes(single_news["content_html"])
            formatted_content = add_backslashes(format_content(content_html))
            title = add_backslashes(single_news["title"])

            news = News(
                id_on_tibiacom=single_news["id"],
                url_tibiacom=single_news["url"],
                type="news",
                content=content,
                content_html=formatted_content,
                date_added=date,
                news_title=title,
            )
            obj.append(news)
        News.objects.bulk_create(obj)


# # # # # # # News end # # # # # # #


# # # # # # # Boosted creature/boss # # # # # # #


# adds boosted boss to database
def add_boss_to_db():
    boss_info = dataapi.boosted_boss()
    category = "boss"

    # check if list is not empty
    if boss_info:
        date = date_with_seconds()

        boss = Boosted(
            name=boss_info["name"],
            image_url=boss_info["image_url"],
            type=category,
            date_time=date,
        )
        boss.save()


# adds boosted creature to database
def add_creature_to_db():
    creature_info = dataapi.boosted_creature()
    category = "creature"

    # check if list is not empty
    if creature_info:
        date = date_with_seconds()

        creature = Boosted(
            name=creature_info["name"],
            image_url=creature_info["image_url"],
            type=category,
            date_time=date,
        )
        creature.save()


# # # # # # # Boosted creature/boss end # # # # # # #


# # # # # # # Worlds # # # # # # #


def add_worlds_information_to_db():
    worlds_information = dataapi.get_worlds_information()
    worlds_latest = pd.DataFrame(data=worlds_information)

    db_worlds = World.objects.all().values()
    db_worlds = pd.DataFrame(data=db_worlds)

    world_list_new = worlds_latest["name"].values.tolist()
    world_list_db = db_worlds["name"].values.tolist()

    not_existing_worlds_list = [
        x for x in world_list_new if x not in world_list_db
    ]
    if not_existing_worlds_list:
        values = {
            "beprotection": {
                "Any World": "-1",
                "Unprotected": "0",
                "Protected": "1",
                "Initially Protected": "2",
            },
            "pvp_type": {
                "Open PvP": "0",
                "Optional PvP": "1",
                "Hardcore PvP": "2",
                "Retro Open PvP": "3",
                "Retro Hardcore PvP": "4",
            },
        }

        obj_worlds = []
        for world in worlds_information:
            if world["name"] in not_existing_worlds_list:
                # getting data of creation date
                if world["battleye_date"] == "release":
                    world_details = dataapi.get_world_details(world["name"])
                    date = world_details["creation_date"] + "-01"
                    battleye_value = values["beprotection"][
                        "Initially Protected"
                    ]
                    creation_date = date
                elif world["battleye_date"] == "":
                    world_details = dataapi.get_world_details(world["name"])
                    date = world_details["creation_date"] + "-01"
                    battleye_value = values["beprotection"]["Unprotected"]
                    creation_date = date
                else:
                    world_details = dataapi.get_world_details(world["name"])
                    date = world["battleye_date"]
                    battleye_value = values["beprotection"]["Protected"]
                    creation_date = world_details["creation_date"] + "-01"

                # add value based on location
                if world["location"] == "Europe":
                    location_value = 0
                elif world["location"] == "South America":
                    location_value = 1
                else:
                    location_value = 2

                world_new = World(
                    name=world["name"],
                    name_value=world["name"],
                    pvp_type=world["pvp_type"],
                    pvp_type_value=values["pvp_type"][world["pvp_type"]],
                    battleye_protected=world["battleye_protected"],
                    battleye_date=date,
                    battleye_value=battleye_value,
                    location=world["location"],
                    location_value=location_value,
                    creation_date=creation_date,
                )
                obj_worlds.append(world_new)

        World.objects.bulk_create(obj_worlds)


def add_world_online_history():
    worlds_information_api = dataapi.get_worlds_information()
    world_id = World.objects.all().values("name", "world_id")
    world_id_df = pd.DataFrame(data=world_id)
    worlds_id_dict = world_id_df.set_index("name")["world_id"].to_dict()

    date = date_with_seconds()
    obj = []
    for world in worlds_information_api:
        players_online = WorldOnlineHistory(
            world_id=worlds_id_dict[world["name"]],
            players_online=world["players_online"],
            date=date,
        )
        obj.append(players_online)
    WorldOnlineHistory.objects.bulk_create(obj)


def add_online_players():
    pass


# # # # # # # Worlds end # # # # # # #


# # # # # # # Experience # # # # # # #


def get_highscores(category: str, proffesions: list):
    # getting world list ( name = value , for now )
    world_list_from_db = World.objects.all().values("name_value")
    world_list_df = pd.DataFrame(data=world_list_from_db)
    worlds = world_list_df["name_value"].tolist()

    # empty df assignment
    result_df = pd.DataFrame

    # for loop for each world
    for world in worlds:
        # for loop for each profession
        for prof in proffesions:
            # get total site number before execution loop over each site

            # 1-20 sites are possible
            request_from_api = dataapi.get_highscores(world, category, prof, 1)
            site_num = request_from_api["highscore_page"]["total_pages"]

            # check if there is more than 20 sites
            if site_num >= 20:
                site_num = 20

            # perform collecting data from api for each vocation
            for i in range(1, site_num + 1):
                request_from_api = dataapi.get_highscores(
                    world, category, prof, i
                )
                if i == 1 and world == worlds[0] and prof == proffesions[0]:
                    result_df = pd.DataFrame(
                        data=request_from_api["highscore_list"]
                    )
                else:
                    result_df = pd.concat(
                        [
                            result_df,
                            pd.DataFrame(
                                data=request_from_api["highscore_list"]
                            ),
                        ],
                        ignore_index=True,
                    )
    # returning collected data in df
    return result_df


# collect data about vocation from db
def collect_voc_id():
    voc = Vocation.objects.all().values("voc_id", "name")
    voc_df = pd.DataFrame(data=voc)
    formatted_voc_data = {}
    voc_dict = voc_df.to_dict("records")

    for i in voc_dict:
        formatted_voc_data.update({i["name"]: i["voc_id"]})

    return formatted_voc_data


# collect data about worlds from db
def collect_world_id():
    world = World.objects.all().values("world_id", "name")
    world_df = pd.DataFrame(data=world)
    formatted_world_data = {}
    world_dict = world_df.to_dict("records")

    for i in world_dict:
        formatted_world_data.update({i["name"]: i["world_id"]})

    return formatted_world_data


# collect data about character from db
def collect_char_id():
    characters = Character.objects.all().values("id_char", "name")
    characters_df = pd.DataFrame(data=characters)
    formatted_characters_data = {}
    characters_dict = characters_df.to_dict("records")

    for i in characters_dict:
        formatted_characters_data.update({i["name"]: i["id_char"]})

    return formatted_characters_data


def save_to_json(item, file_name):
    path_to_directory = f"{tibia_stats.settings.TEMP_DIR}"
    full_path = "".join([path_to_directory, file_name])
    write = json.dumps(item)

    with open(full_path, "w") as f:
        f.write(write)


def read_json(file_name):
    path_to_directory = f"{tibia_stats.settings.TEMP_DIR}"
    full_path = "".join([path_to_directory, file_name])

    with open(full_path, "r") as file:
        json_data = json.load(file)

    return json_data


def save_to_file(item, file_name):
    path_to_directory = f"{tibia_stats.settings.TEMP_DIR}"
    raw_file = "".join([date_for_files(), "-", file_name, ".csv"])

    full_path = "".join([path_to_directory, raw_file])
    item.to_csv(path_or_buf=full_path, mode="w", index=False)


def read_file(file_name):
    path_to_directory = f"{tibia_stats.settings.TEMP_DIR}"
    raw_file = "".join([date_for_files(), "-", file_name, ".csv"])
    full_path = "".join([path_to_directory, raw_file])

    file_df = pd.read_csv(
        filepath_or_buffer=full_path, index_col=False, memory_map=True
    )
    return file_df


def date_for_files():
    return datetime.datetime.now().strftime("%d%m%Y")


def scrap_experience(date):
    logging.info(f"{date_with_seconds()} - started exp scrapping")
    category_exp = "experience"
    prof_for_exp = ["none", "knights", "paladins", "sorcerers", "druids"]
    latest_highscores = get_highscores(category_exp, prof_for_exp)
    save_to_file(latest_highscores, "raw_exp")
    Tasks.objects.filter(task_name="scrap_experience").update(status="done")
    logging.info(f"{date_with_seconds()} - Exp saved.")
    # return latest_highscores


def scrap_charms(date):
    logging.info(f"{date_with_seconds()} - started charm scrapping")
    category_charms = "charmpoints"
    prof_for_charms = ["knights", "paladins", "sorcerers", "druids"]
    latest_charms = get_highscores(category_charms, prof_for_charms)
    save_to_file(latest_charms, "raw_charms")
    Tasks.objects.filter(task_name="scrap_charms").update(status="done")
    logging.info(f"{date_with_seconds()} - Charms saved.")
    # return latest_charms


def prepare_data_and_db(date):
    logging.info(f"Preparing data started: {date_with_seconds()}")

    yesterday = Highscores.objects.all().order_by('-date').values('date')[:1]

    latest_highscores = read_file("raw_exp")
    latest_charms = read_file("raw_charms")

    latest_highscores = latest_highscores[latest_highscores["level"] > 20]
    latest_charms = latest_charms[latest_charms["level"] > 20]

    chars_id = collect_char_id()
    latest_highscores["name_id_db"] = (
        latest_highscores["name"].map(chars_id).fillna(0)
    )
    latest_charms["name_id_db"] = latest_charms["name"].map(chars_id).fillna(0)

    world_id = collect_world_id()
    latest_highscores["world"].update(latest_highscores["world"].map(world_id))
    latest_charms["world"].update(latest_charms["world"].map(world_id))

    voc_id = collect_voc_id()
    latest_highscores["vocation"].update(
        latest_highscores["vocation"].map(voc_id)
    )
    latest_charms["vocation"].update(latest_charms["vocation"].map(voc_id))

    exp_without_id = latest_highscores[latest_highscores["name_id_db"] == 0]
    charms_without_id = latest_charms[latest_charms["name_id_db"] == 0]

    name_list_dont_exist1 = exp_without_id["name"].values.tolist()
    name_list_dont_exist2 = charms_without_id["name"].values.tolist()
    name_list_dont_exist = name_list_dont_exist1 + name_list_dont_exist2
    name_list_dont_exist = list(set(name_list_dont_exist))

    checked = Tasks.objects.filter(task_name="checked_characters").values(
        "status"
    )[:1]

    if checked and (checked[0]["status"] == "done"):
        names = read_json("checked.txt")
        logging.info(f"Names readed from checked.txt file.")
    else:
        names = check_characters_at_tibiacom(name_list_dont_exist)
        logging.info(f"Names checked on tibia.com")

    new_players = names["new_players"]
    name_change = names["name_change"]
    # deleted_characters = names["deleted_characters"]

    old_name_list = [value for key, value in name_change.items()]

    if name_change:
        update_character(name_change)
        logging.info(
            f"Update character completed. Updated {len(name_change)} characters"
        )

    latest_highscores.drop("name_id_db", axis=1, inplace=True)
    latest_charms.drop("name_id_db", axis=1, inplace=True)
    chars_id = collect_char_id()
    latest_highscores["name_id_db"] = (
        latest_highscores["name"].map(chars_id).fillna(0).astype("int64")
    )
    latest_charms["name_id_db"] = (
        latest_charms["name"].map(chars_id).fillna(0).astype("int64")
    )

    exp_after_up = latest_highscores[latest_highscores["name_id_db"] == 0]
    charm_after_up = latest_charms[latest_charms["name_id_db"] == 0]
    exp_after_up = exp_after_up["name"].values.tolist()
    charm_after_up = charm_after_up["name"].values.tolist()
    check_chars = exp_after_up + charm_after_up + new_players
    new_players = list(set(check_chars))

    if new_players:
        insert_new_players(latest_highscores, latest_charms, new_players)
    logging.info(f"Inserted {len(new_players)} new players.")

    latest_highscores.drop("name_id_db", axis=1, inplace=True)
    latest_charms.drop("name_id_db", axis=1, inplace=True)

    chars_id = collect_char_id()
    latest_highscores["id_char"] = latest_highscores["name"].map(chars_id)
    latest_charms["id_char"] = latest_charms["name"].map(chars_id)

    logging.info(f"{date_with_seconds()} - Name change preparing data.")
    if name_change:
        name_change_exp = latest_highscores[
            latest_highscores["name"].isin(old_name_list)
        ]
        name_change_charm = latest_charms[
            latest_charms["name"].isin(old_name_list)
        ]
        name_change_df = pd.concat([name_change_charm, name_change_exp])
        name_change_df = name_change_df.drop_duplicates("name")
        save_to_file(name_change_df, "name_changes_df")

        old_name = dict((v, k) for k, v in name_change.items())
        save_to_json(old_name, "name_changes.txt")
        logging.info(f"File saved.")

    all_chars = latest_highscores.merge(
        latest_charms, on="id_char", how="outer", suffixes=("_exp", "_charm")
    )
    all_chars.fillna(0, inplace=True)

    del latest_highscores
    del latest_charms
    gc.collect()

    if all_chars.isnull().values.any():
        raise ValueError(f"NaN found... {all_chars.isnull().sum().any()}")

    all_chars = all_chars.astype(
        {
            "rank_exp": "int64",
            "vocation_exp": "int64",
            "vocation_charm": "int64",
            "world_charm": "int64",
            "level_exp": "int64",
            "world_exp": "int64",
            "value_exp": "int64",
            "rank_charm": "int64",
            "value_charm": "int64",
            "level_charm": "int64",
            "id_char": "int64",
        }
    )

    all_chars.loc[all_chars["vocation_exp"] == 0, "vocation_exp"] = all_chars[
        "vocation_charm"
    ]
    all_chars.loc[all_chars["world_exp"] == 0, "world_exp"] = all_chars[
        "world_charm"
    ]
    all_chars.loc[(all_chars["name_exp"] == 0), "name_exp"] = all_chars[
        "name_charm"
    ]
    all_chars.loc[all_chars["level_exp"] == 0, "level_exp"] = all_chars[
        "level_charm"
    ]

    all_chars.drop(
        columns=[
            "level_charm",
            "world_charm",
            "vocation_charm",
            "name_charm",
        ],
        axis=1,
        inplace=True,
    )

    all_chars = all_chars.drop_duplicates("name_exp", keep="last")

    all_chars.rename(
        columns={
            "name_exp": "name",
            "rank_exp": "exp_rank",
            "vocation_exp": "voc_id",
            "world_exp": "world_id",
            "level_exp": "level",
            "value_exp": "exp_value",
            "rank_charm": "charm_rank",
            "value_charm": "charm_value",
        },
        inplace=True,
    )

    old_highscores_query = (
        Highscores.objects.all()
        .filter(Q(date__gte=yesterday))
        .values(
            "exp_rank",
            "id_char",
            "id_char__name",
            "world_id",
            "level",
            "exp_value",
            "charm_rank",
            "charm_value",
        )
    )
    old_highscores_df = pd.DataFrame(data=old_highscores_query)

    prep_for_bulk = old_highscores_df.merge(
        all_chars, on="id_char", how="outer", suffixes=("_db", "_new")
    )

    del all_chars
    del old_highscores_df
    gc.collect()
    prep_for_bulk.fillna(0, inplace=True)

    prep_for_bulk = prep_for_bulk.drop_duplicates("id_char", keep="last")

    prep_for_bulk = prep_for_bulk.astype(
        {
            "exp_rank_db": "int64",
            "world_id_db": "int64",
            "level_db": "int64",
            "exp_value_db": "int64",
            "charm_rank_db": "int64",
            "charm_value_db": "int64",
            "exp_rank_new": "int64",
            "voc_id": "int64",
            "world_id_new": "int64",
            "level_new": "int64",
            "exp_value_new": "int64",
            "charm_rank_new": "int64",
            "charm_value_new": "int64",
        }
    )

    world_transfers = prep_for_bulk[
        prep_for_bulk["world_id_db"] != prep_for_bulk["world_id_new"]
    ]
    world_transfers = world_transfers[
        (world_transfers["world_id_new"] != 0)
        & (world_transfers["world_id_db"] != 0)
    ]

    if not world_transfers.isnull().values.any():
        save_to_file(world_transfers, "world_transfers")
        logging.info(f"World transfers file saved.")

    prep_for_bulk["exp_diff"] = np.where(
        (prep_for_bulk["exp_value_db"] != 0)
        & (prep_for_bulk["exp_value_new"] != 0),
        prep_for_bulk["exp_value_new"] - prep_for_bulk["exp_value_db"],
        0,
    )

    prep_for_bulk["exp_rank_change"] = np.where(
        (prep_for_bulk["exp_rank_db"] != 0)
        & (prep_for_bulk["exp_rank_new"] != 0),
        prep_for_bulk["exp_rank_db"] - prep_for_bulk["exp_rank_new"],
        0,
    )

    prep_for_bulk["level_change"] = (
        prep_for_bulk["level_new"] - prep_for_bulk["level_db"]
    )

    prep_for_bulk["charm_rank_change"] = np.where(
        (prep_for_bulk["charm_rank_db"] != 0)
        & (prep_for_bulk["charm_rank_new"] != 0),
        prep_for_bulk["charm_rank_db"] - prep_for_bulk["charm_rank_new"],
        0,
    )

    prep_for_bulk["charm_diff"] = np.where(
        (prep_for_bulk["charm_value_db"] != 0)
        & (prep_for_bulk["charm_value_new"] != 0),
        prep_for_bulk["charm_value_new"] - prep_for_bulk["charm_value_db"],
        0,
    )

    prep_for_bulk = prep_for_bulk.astype(
        {
            "exp_diff": "int64",
            "charm_diff": "int64",
            "exp_rank_change": "int64",
            "charm_rank_change": "int64",
        }
    )

    prep_for_bulk = prep_for_bulk.drop_duplicates("id_char", keep="last")

    save_to_file(prep_for_bulk, "prep_for_bulk")
    Tasks.objects.filter(task_name="prepare_data_and_db").update(status="done")
    logging.info(
        f"{len(prep_for_bulk)} characters prepared for insert. File saved."
    )


# ================== check_characters ====================
def check_characters_at_tibiacom(name_list_dont_exist):
    logging.info(f"{date_with_seconds()} - started checking characters.")
    new_players = []
    name_change = {}
    deleted_characters = []
    for i in name_list_dont_exist:
        char = dataapi.get_character_info(i)
        if char["character"]["name"] == "":
            # character is deleted
            deleted_characters.append(i)
        elif "former_names" in char["character"]:
            old_name = char["character"]["former_names"][-1]
            new_name = char["character"]["name"]
            name_change.update({old_name: new_name})
        else:
            new_players.append(char["character"]["name"])
    character_names = {
        "new_players": new_players,
        "name_change": name_change,
        "deleted_characters": deleted_characters,
    }

    save_to_json(character_names, "checked.txt")
    task_name = Tasks(
        task_name="checked_characters", status="done", date=date_with_seconds()
    )
    task_name.save()
    logging.info(
        f"{date_with_seconds()} - saved and updated task status in db."
    )
    return character_names


# === INSERT =============== NAME CHANGE ====================
def insert_name_change(date):
    name_change_df = read_file("name_changes_df")
    old_name = read_json("name_changes.txt")

    name_change_dict = name_change_df.to_dict("index")
    obj_name_change = []
    traded = 0  # temp variable
    for name_in_dict in name_change_dict:
        name = NameChange(
            id_char_id=name_change_dict[name_in_dict]["id_char"],
            old_name=old_name[name_change_dict[name_in_dict]["name"]],
            new_name=name_change_dict[name_in_dict]["name"],
            level=name_change_dict[name_in_dict]["level"],
            traded=traded,
            date=date,
        )
        obj_name_change.append(name)
    NameChange.objects.bulk_create(obj_name_change, batch_size=500)
    Tasks.objects.filter(task_name="insert_name_change").update(status="done")


# === INSERT =============== New players ====================
def insert_new_players(latest_highscores, latest_charms, new_players):
    logging.info(f"Insert new players started: {date_with_seconds()}")
    new_characters_in_exp = latest_highscores[
        latest_highscores["name"].isin(new_players)
    ]
    new_characters_in_charms = latest_charms[
        latest_charms["name"].isin(new_players)
    ]
    new_characters = pd.concat(
        [new_characters_in_charms, new_characters_in_exp]
    )
    new_characters.reset_index(drop=True, inplace=True)
    new_characters_dict = new_characters.to_dict("index")
    char_to_insert = []

    for item in new_characters_dict:
        char_ready_to_bulk = Character(
            name=new_characters_dict[item]["name"],
            world_id=new_characters_dict[item]["world"],
            voc_id=new_characters_dict[item]["vocation"],
        )
        char_to_insert.append(char_ready_to_bulk)

    Character.objects.bulk_create(char_to_insert, batch_size=100)
    logging.info(f"Insert new players ended: {date_with_seconds()}")


# === INSERT =============== WORLD CHANGE ====================
def insert_world_changes(date):
    logging.info(f"Insert world changes started: {date_with_seconds()}")
    world_transfers = read_file("world_transfers")

    id_to_world = {}
    world_id = collect_world_id()
    for key, value in world_id.items():
        id_to_world.update({value: key})

    obj_world = []
    traded = 0  # temp variable
    world_transfers_dict = world_transfers.to_dict("index")

    for i in world_transfers_dict:
        transfer = WorldTransfers(
            id_char_id=world_transfers_dict[i]["id_char"],
            old_world=id_to_world[world_transfers_dict[i]["world_id_db"]],
            oldid=world_transfers_dict[i]["world_id_db"],
            new_world=id_to_world[world_transfers_dict[i]["world_id_new"]],
            newid=world_transfers_dict[i]["world_id_new"],
            level=world_transfers_dict[i]["level_new"],
            traded=traded,
            date=date,
        )
        obj_world.append(transfer)
    WorldTransfers.objects.bulk_create(obj_world, batch_size=500)
    Tasks.objects.filter(task_name="insert_world_changes").update(
        status="done"
    )
    logging.info(
        f"{len(world_transfers_dict)}world transfers inserted. \n"
        f" End: {date_with_seconds()}"
    )


def update_character(name_change):
    logging.info(f"UPDATE started: {date_with_seconds()}")
    for key, value in name_change.items():
        Character.objects.filter(name=key).update(name=value)
    logging.info(
        f"UPDATE ended: {date_with_seconds()} updated: {len(name_change)} names."
    )


def insert_highscores(date):
    logging.info(f"Highscores insert started: {date_with_seconds()}")
    prep_for_bulk = read_file("prep_for_bulk")

    obj = []
    prep_for_bulk = prep_for_bulk.loc[
        (prep_for_bulk["voc_id"] != 0)
        & (prep_for_bulk["world_id_new"] != 0)
        & (prep_for_bulk["id_char"] != 0)
    ]

    if not prep_for_bulk.isnull().values.any():
        inner_data_dict = prep_for_bulk.to_dict("index")

        del prep_for_bulk
        gc.collect()

        db_count = Highscores.objects.all().count()
        amouont_for_insert = len(inner_data_dict)

        for index, i in enumerate(inner_data_dict):
            char = Highscores(
                exp_rank=inner_data_dict[i]["exp_rank_new"],
                exp_rank_change=inner_data_dict[i]["exp_rank_change"],
                id_char_id=inner_data_dict[i]["id_char"],
                voc_id=inner_data_dict[i]["voc_id"],
                world_id=inner_data_dict[i]["world_id_new"],
                level=inner_data_dict[i]["level_new"],
                level_change=inner_data_dict[i]["level_change"],
                exp_value=inner_data_dict[i]["exp_value_new"],
                exp_diff=inner_data_dict[i]["exp_diff"],
                charm_rank=inner_data_dict[i]["charm_rank_new"],
                charm_rank_change=inner_data_dict[i]["charm_rank_change"],
                charm_value=inner_data_dict[i]["charm_value_new"],
                charm_diff=inner_data_dict[i]["charm_diff"],
                date=date,
            )
            obj.append(char)

            if index % 3000 == 0:
                Highscores.objects.bulk_create(obj, batch_size=500)
                obj = []
            if index == len(inner_data_dict) - 1:
                Highscores.objects.bulk_create(obj, batch_size=200)

        db_count_after_insert = Highscores.objects.all().count()
        if db_count_after_insert == db_count + amouont_for_insert:
            logging.info(f"Successfully added: {amouont_for_insert}")
        else:
            logging.info(
                f"Actual amount of items: {db_count_after_insert}."
                f"Items that should be added: {amouont_for_insert}."
            )
        Tasks.objects.filter(task_name="insert_highscores").update(
            status="done"
        )
        logging.info(f"Insert end: {date_with_seconds()}")


def add_highscores():
    pass
    # date = "2023-02-01 05:00:00"


def get_daily_records(date):
    # best exp yesterday on each world
    yesterday = date - timedelta(days=1, hours=2)

    # world_types = {
    #    0: 'Open PvP',
    #    1: 'Optional PvP',
    #    3: 'Retro Open PvP',
    #    4: 'Retro Hardcore PvP'
    # }

    # getting world list id
    world_list_from_db = World.objects.all().values("world_id")
    world_list_df = pd.DataFrame(data=world_list_from_db)
    worlds = world_list_df["world_id"].tolist()

    # getting vocation list id
    vocation_list_from_db = Vocation.objects.all().values("voc_id")
    vocation_list_df = pd.DataFrame(data=vocation_list_from_db)
    vocations = vocation_list_df["voc_id"].tolist()

    # getting the best exp (each vocation on every world)
    best = Highscores.objects.filter(
        Q(date__gt=yesterday) & (Q(exp_diff__gt="0") | Q(exp_diff__lt="0"))
    ).values(
        "exp_rank",
        "exp_rank_change",
        "id_char",
        "voc_id",
        "world_id",
        "level",
        "level_change",
        "exp_value",
        "exp_diff",
        "charm_rank",
        "charm_rank_change",
        "charm_value",
        "charm_diff",
        "date",
    )
    db_data_to_df = pd.DataFrame(data=best)

    # best experience gained
    for world in worlds:
        for vocation in vocations:
            best_exp = (
                db_data_to_df[
                    (db_data_to_df["world_id"] == world)
                    & (db_data_to_df["voc_id"] == vocation)
                ]
                .sort_values(by="exp_diff")
                .tail(1)
            )

            if world == 1 and vocation == 1:
                history_best_exp = best_exp
            else:
                history_best_exp = pd.concat(
                    [best_exp, history_best_exp], ignore_index=True
                )

    # biggest lost experience
    for world in worlds:
        for vocation in vocations:
            worst_exp = (
                db_data_to_df[
                    (db_data_to_df["world_id"] == world)
                    & (db_data_to_df["voc_id"] == vocation)
                    & (db_data_to_df["exp_diff"] < 0)
                ]
                .sort_values(by="exp_diff")
                .head(1)
            )
            if world == 1 and vocation == 1:
                history_worst_exp = worst_exp
            else:
                history_worst_exp = pd.concat(
                    [worst_exp, history_worst_exp], ignore_index=True
                )

    for world in worlds:
        for vocation in vocations:
            if vocation != 0:
                best_charm = (
                    db_data_to_df[
                        (db_data_to_df["world_id"] == world)
                        & (db_data_to_df["voc_id"] == vocation)
                    ]
                    .sort_values(by="charm_diff")
                    .tail(1)
                )

            if world == 1 and vocation == 1:
                history_best_charm = best_charm
            else:
                history_best_charm = pd.concat(
                    [best_charm, history_best_charm], ignore_index=True
                )

    history = pd.concat(
        [history_worst_exp, history_best_charm, history_best_exp],
        ignore_index=True,
    )

    record_type = "exp"
    event = "none"

    db_record_history_count_before = RecordsHistory.objects.all().count()

    history_dict = history.to_dict("index")

    del history
    gc.collect()

    obj = []
    for i in history_dict:
        record = RecordsHistory(
            exp_rank=history_dict[i]["exp_rank"],
            exp_rank_change=history_dict[i]["exp_rank_change"],
            id_char_id=history_dict[i]["id_char"],
            voc_id=history_dict[i]["voc_id"],
            world_id=history_dict[i]["world_id"],
            level=history_dict[i]["level"],
            level_change=history_dict[i]["level_change"],
            exp_value=history_dict[i]["exp_value"],
            exp_diff=history_dict[i]["exp_diff"],
            charm_rank=history_dict[i]["charm_rank"],
            charm_rank_change=history_dict[i]["charm_rank_change"],
            charm_value=history_dict[i]["charm_value"],
            charm_diff=history_dict[i]["charm_diff"],
            record_type=record_type,
            event=event,
            date=date,
        )
        obj.append(record)
    RecordsHistory.objects.bulk_create(obj)

    db_record_history_count_after = RecordsHistory.objects.all().count()
    Tasks.objects.filter(task_name="get_daily_records").update(status="done")
    if (
        db_record_history_count_after
        == len(obj) + db_record_history_count_before
    ):
        logging.info(f"Successfully added {len(obj)} items to db.")
    else:
        logging.info(f"Some records might be missing. Added {len(obj)} to db.")
    logging.info(
        f"# # END # # # # {date_with_seconds()} # # # # Daily records # # # # # #"
    )


def move_only_active_players(date):
    logging.info(
        f"# # START # # # # {date_with_seconds()} # # # # ACTIVE PLAYERS # # # # #"
    )
    yesterday = date - timedelta(days=1)

    only_active = Highscores.objects.filter(
        Q(date__gt=yesterday) & (Q(exp_diff__gt="0") | Q(exp_diff__lt="0"))
    ).values()
    only_active_df = pd.DataFrame(data=only_active)

    del only_active
    gc.collect()

    db_active_before = HighscoresHistory.objects.all().count()

    obj = []
    only_active_dict = only_active_df.to_dict("index")

    del only_active_df
    gc.collect()

    for index, i in enumerate(only_active_dict):
        char = HighscoresHistory(
            exp_rank=only_active_dict[i]["exp_rank"],
            exp_rank_change=only_active_dict[i]["exp_rank_change"],
            id_char_id=only_active_dict[i]["id_char_id"],
            voc_id=only_active_dict[i]["voc_id"],
            world_id=only_active_dict[i]["world_id"],
            level=only_active_dict[i]["level"],
            level_change=only_active_dict[i]["level_change"],
            exp_value=only_active_dict[i]["exp_value"],
            exp_diff=only_active_dict[i]["exp_diff"],
            charm_rank=only_active_dict[i]["charm_rank"],
            charm_rank_change=only_active_dict[i]["charm_rank_change"],
            charm_value=only_active_dict[i]["charm_value"],
            charm_diff=only_active_dict[i]["charm_diff"],
            date=date,
        )
        obj.append(char)
        if index % 3000 == 0:
            HighscoresHistory.objects.bulk_create(obj, 500)
            obj = []
        if index == len(only_active_dict) - 1:
            HighscoresHistory.objects.bulk_create(obj, 500)

    db_active_after = HighscoresHistory.objects.all().count()
    Tasks.objects.filter(task_name="move_only_active_players").update(
        status="done"
    )
    if db_active_after == len(obj) + db_active_before:
        logging.info(f"Successfully added {len(obj)} items to db history.")
    else:
        logging.info(
            f"Some records might be missing. Added {len(obj)} to db history."
        )


def delete_old_highscores_date(date):
    date = date - timedelta(days=2, hours=2)

    clear_data_query = Highscores.objects.filter(date__lt=date)
    clear_data_query._raw_delete(clear_data_query.db)
    Tasks.objects.filter(task_name="delete_old_highscores_date").update(
        status="done"
    )


# # # # # # # Experience end # # # # # # #

# # # # # # # Kill statistics start # # # # # # #

def get_creature_kill_stats():
    date = datetime.datetime.now()

    world_list = (
        World.objects.all().values("name_value", "world_id").order_by("name")
    )
    world_df = pd.DataFrame(world_list)
    world_dict = world_df.set_index("name_value")["world_id"].to_dict()
    world_list = world_df["name_value"].values.tolist()

    all_bosses = Bosses.objects.all().values("id", "name", "disp_name")
    bosses_df = pd.DataFrame(all_bosses)

    all_monsters = Monsters.objects.all().values("id", "name", "disp_name")
    monsters_df = pd.DataFrame(all_monsters)

    bosses_for_bulk = pd.DataFrame()
    monsters_for_bulk = pd.DataFrame()

    for world in world_list:
        kill_stats_raw_df = get_data_in_df(world)

        # MONSTERS
        monsters_data = cleanup_and_prep_monsters(
            kill_stats_raw_df, date, world, world_dict, monsters_df
        )
        monsters_for_bulk = pd.concat([monsters_for_bulk, monsters_data])

        # BOSSES
        bosses_seen = cleanup_and_prep_bosses(
            kill_stats_raw_df, date, world, world_dict, bosses_df
        )
        bosses_for_bulk = pd.concat([bosses_for_bulk, bosses_seen])

    bosses_for_bulk.reset_index(inplace=True, drop=True)
    monsters_for_bulk.reset_index(inplace=True, drop=True)

    bulk_bosses(bosses_for_bulk)
    bulk_monsters(monsters_for_bulk)
    # # todo some logs


def get_data_in_df(world):
    kill_stats_raw = dataapi.get_kill_statistics(world)
    kill_stats_raw_df = pd.DataFrame(kill_stats_raw)

    kill_stats_raw_df.drop(
        columns=[
            "last_week_players_killed",
            "last_week_killed",
        ],
        axis=1,
        inplace=True,
    )
    kill_stats_raw_df.rename(
        columns={
            "race": "disp_name",
        },
        inplace=True,
    )
    return kill_stats_raw_df


def cleanup_and_prep_monsters(
    kill_stats_raw_df, date, world, world_dict, monsters_df
):
    monsters_all = kill_stats_raw_df[
        kill_stats_raw_df["disp_name"].str.islower()
    ]

    monsters_with_s = monsters_all[
        monsters_all["disp_name"].str[-1] == "s"
    ].copy()
    monsters_removed_s = monsters_with_s.apply(
        lambda x: x.str.slice(stop=-1) if x.dtype == "object" else x
    )

    monsters_without_s = monsters_all[
        monsters_all["disp_name"].str[-1] != "s"
    ].copy()

    monsters_with_ies = monsters_without_s[
        monsters_without_s["disp_name"].str.split().str[0].str[-3:] == "ies"
    ].copy()
    monsters_with_ies_list = monsters_with_ies["disp_name"].tolist()

    monsters_with_ies["disp_name"] = monsters_with_ies[
        "disp_name"
    ].str.replace("ies", "y")
    monsters_removed_ies = monsters_with_ies

    all_without_ies = monsters_without_s[
        ~monsters_without_s["disp_name"].isin(monsters_with_ies_list)
    ].copy()

    s_in_first_word = all_without_ies[
        all_without_ies["disp_name"].str.split().str[0].str[-1] == "s"
    ].copy()
    no_s = all_without_ies[
        all_without_ies["disp_name"].str.split().str[0].str[-1] != "s"
    ].copy()

    list_of_monsters = s_in_first_word["disp_name"].values.tolist()
    new_dict = {}
    for i in list_of_monsters:
        x = i.split()
        x[0] = x[0][:-1]
        x = " ".join(x)
        new_dict.update({i: x})

    s_in_first_word["disp_name"].update(
        s_in_first_word["disp_name"].map(new_dict)
    )

    to_concat = [
        monsters_removed_ies,
        monsters_removed_s,
        no_s,
        s_in_first_word,
    ]

    all_monsters_after_prep = pd.concat(to_concat)
    all_monsters_after_prep.reset_index(inplace=True, drop=True)

    monsters_df["name"] = monsters_df["name"].str.replace("_", " ")
    all_monsters_after_prep.rename(columns={"disp_name": "name"}, inplace=True)
    monsters_df = monsters_df.merge(all_monsters_after_prep, on="name")

    monsters_df.drop(
        columns=[
            "name",
            "disp_name",
        ],
        axis=1,
        inplace=True,
    )
    monsters_df.rename(
        columns={
            "last_day_players_killed": "killed_players",
            "last_day_killed": "killed",
            "id": "monster",
        },
        inplace=True,
    )
    monsters_df["world"] = world
    monsters_df["date"] = date
    monsters_df.replace({"world": world_dict}, inplace=True)
    monsters_df = monsters_df.loc[(monsters_df['killed'] > 0) | (monsters_df['killed_players'] > 0)]

    return monsters_df


def cleanup_and_prep_bosses(
    kill_stats_raw_df, date, world, world_dict, bosses_df
):
    bosses_seen = bosses_df.merge(kill_stats_raw_df, on="disp_name")
    bosses_seen.drop(
        columns=[
            "name",
            "disp_name",
        ],
        axis=1,
        inplace=True,
    )
    bosses_seen.rename(
        columns={
            "last_day_players_killed": "killed_players",
            "last_day_killed": "killed",
            "id": "boss",
        },
        inplace=True,
    )
    bosses_seen["world"] = world
    bosses_seen["date"] = date
    bosses_seen.replace({"world": world_dict}, inplace=True)
    bosses_seen = bosses_seen.loc[
        (bosses_seen['killed'] > 0) | (bosses_seen['killed_players'] > 0)]

    return bosses_seen


def bulk_bosses(bosses_for_bulk):
    obj_bosses = []
    bosses_for_bulk_dict = bosses_for_bulk.to_dict("index")

    for i in bosses_for_bulk_dict:
        boss = BossStats(
            boss_id=bosses_for_bulk_dict[i]['boss'],
            killed_players=bosses_for_bulk_dict[i]['killed_players'],
            killed=bosses_for_bulk_dict[i]['killed'],
            world_id=bosses_for_bulk_dict[i]['world'],
            date=bosses_for_bulk_dict[i]['date'],
        )
        obj_bosses.append(boss)

    BossStats.objects.bulk_create(obj_bosses, batch_size=500)


def bulk_monsters(monsters_for_bulk):
    obj_monster = []
    monsters_for_bulk_dict = monsters_for_bulk.to_dict("index")

    for i in monsters_for_bulk_dict:
        monster = MonsterStats(
            monster_id=monsters_for_bulk_dict[i]["monster"],
            killed_players=monsters_for_bulk_dict[i]["killed_players"],
            killed=monsters_for_bulk_dict[i]["killed"],
            world_id=monsters_for_bulk_dict[i]["world"],
            date=monsters_for_bulk_dict[i]["date"],
        )
        obj_monster.append(monster)

    MonsterStats.objects.bulk_create(obj_monster, batch_size=500)

# # # # # # # Kill statistics end # # # # # # #


if __name__ == "__main__":
    main()
