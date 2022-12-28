from django.shortcuts import render
from django.db import connection
from .models import News, Boosted, World, WorldOnlineHistory, Highscores, RecordsHistory
from datetime import datetime, timedelta
import datetime
from pathlib import Path
import os
import json
import pandas as pd
import scripts.tibiadata_API.get_data as dataapi
from django.db.models import Q


# Main page
def main_page(request, *args, **kwargs):

    # news ticker
    latest_tickers = News.objects.filter(type='ticker').order_by('-news_id')[:3]

    # boosted boss
    boosted_boss = Boosted.objects.filter(type='boss').order_by('-boosted_id')[:1]

    # boosted creature
    boosted_creature = Boosted.objects.filter(type='creature').order_by('-boosted_id')[:1]

    # news
    latest_news = News.objects.filter(type='news').order_by('-news_id')[:4]

    # best exp yesterday on each world
    now = datetime.datetime.now()
    # date = (now - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    date = '2022-12-23 11:11:48'

    # world_types = {
    #    0: 'Open PvP',
    #    1: 'Optional PvP',
    #    3: 'Retro Open PvP',
    #    4: 'Retro Hardcore PvP'
    # }

    best_open_pvp = RecordsHistory.objects.filter(
        Q(date__gt=date)
        & Q(exp_diff__gt=0)
        & Q(world__pvp_type_value=0)
    ).order_by(
        '-exp_diff'
    ).first()

    best_optional_pvp = RecordsHistory.objects.filter(
        Q(date__gt=date)
        & Q(exp_diff__gt=0)
        & Q(world__pvp_type_value=1)
    ).order_by(
        '-exp_diff'
    ).first()

    best_retro_open_pvp = RecordsHistory.objects.filter(
        Q(date__gt=date)
        & Q(exp_diff__gt=0)
        & Q(world__pvp_type_value=3)
    ).order_by(
        '-exp_diff'
    ).first()

    best_retro_hardcore_pvp = RecordsHistory.objects.filter(
        Q(date__gt=date)
        & Q(exp_diff__gt=0)
        & Q(world__pvp_type_value=4)
    ).order_by(
        '-exp_diff'
    ).first()

    content = {
        'news_ticker': latest_tickers,
        'boosted_boss': boosted_boss,
        'boosted_creature': boosted_creature,
        'latest_news': latest_news,
        # 'best_exp': best_exp
        'optional': best_optional_pvp,
        'open': best_open_pvp,
        'retro_open': best_retro_open_pvp,
        'retro_hardcore': best_retro_hardcore_pvp
    }
    return render(request, "sites/index.html", content)


# Error 404
def error404(request, *args, **kwargs):
    return render(request, "sites/404.html")


# Under construction
def under_construction(request, *args, **kwargs):
    return render(request, "sites/under_construction.html")


# Sign in
def sign_in(request, *args, **kwargs):
    return render(request, "sites/sign_in.html")


# Sign up
def sign_up(request, *args, **kwargs):
    return render(request, "sites/sign_up.html")


# # # # # # # # # # # # Worlds # # # # # # # # # # # #

# World main
def worlds_main(request, *args, **kwargs):

    # All worlds
    all_worlds = WorldOnlineHistory.objects\
        .select_related('world')\
        .filter(date__gte=datetime.datetime.now() - datetime.timedelta(seconds=260))

    # Load data for creation chart from json
    path_to_json = Path(__file__).resolve().parent.parent
    creation_chart = json.load(open(os.path.join(path_to_json, 'scripts\\json_files\\creation_chart.json')))

    # Online history chart
    get_online_history = WorldOnlineHistory.objects \
        .select_related('world') \
        .filter(date__gte=datetime.datetime.now() - datetime.timedelta(hours=24)) \
        .values('world__location', 'world_id', 'players_online', 'date')

    df = pd.DataFrame(get_online_history)
    df['hour'] = df['date'].dt.round('H').dt.hour
    df = df.sort_values(by=['date'])
    world = df['world__location'].unique()
    hours = df['hour'].unique()
    online_history = {}
    online_history_all = {}

    for i in world:
        mean_location = {}
        for hour in hours:
            mean_location.update({
                hour: int(df.loc[(df['world__location'] == i) & (df['hour'] == hour), 'players_online'].mean())
            })
            if i == world[-1]:
                online_history_all.update({
                    hour: int(df.loc[df['hour'] == hour, 'players_online'].mean())
                })
        online_history.update({i: mean_location})
    online_history.update({'Total': online_history_all})
    content = {
        'all_worlds': all_worlds,
        'created': creation_chart,
        'online_history': online_history
    }
    return render(request, "sites/worlds/all_worlds.html", content)


# Single world
def single_world(request, name):

    # get data from api
    world_information = dataapi.get_world_details(name)

    # data for chart ( number of online players of each vocation )
    knight, druid, paladin, sorcerer, none = 0, 0, 0, 0, 0
    if world_information['players_online'] != 0:
        for i in world_information['online_players']:
            if i['vocation'] == 'Paladin' or i['vocation'] == 'Royal Paladin':
                paladin += 1
            elif i['vocation'] == 'Druid' or i['vocation'] == 'Elder Druid':
                druid += 1
            elif i['vocation'] == 'Knight' or i['vocation'] == 'Elite Knight':
                knight += 1
            elif i['vocation'] == 'Sorcerer' or i['vocation'] == 'Master Sorcerer':
                sorcerer += 1
            else:
                none += 1

    # data to dictionary
    online_counter = {
        'Knights': knight,
        'Sorcerers': sorcerer,
        'Paladins': paladin,
        'Druids': druid,
        'None': none
    }

    # sort by value (highest > lowest)
    online_counter = {key: value
                      for key, value in sorted(online_counter.items(),
                                               key=lambda item: item[1],
                                               reverse=True)}

    # get world list with id
    world_list = World.objects.all().values('name', 'name_value')

    content = {
        'world': world_information,
        'online': online_counter,
        'world_list': world_list,
    }
    return render(request, "sites/worlds/single_world.html", content)


# # # # # # # # # # # # End Worlds # # # # # # # # # # # #

# # # # # # # # # # Experience # # # # # # # # # # #

def top_500(request, *args, **kwargs):

    # now = datetime.datetime.now()
    # date = (now - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    date = '2022-12-23 11:11:50'

    top = Highscores.objects.filter(
        Q(date__gt=date)
        & Q(exp_diff__gt=0)
    ).order_by(
        '-exp_diff'
    )[:500]

    content = {
        'top': top
    }

    return render(request, "sites/experience/top500.html", content)


def mainland(request, *args, **kwargs):

    # now = datetime.datetime.now()
    # date = (now - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    date = '2022-12-23 11:11:50'
    query = ''
    # get world list with id
    world_list = World.objects.all().values('name', 'name_value', 'world_id')
    main = {}
    if request.GET:
        query = request.GET['q']

        worlds_df = pd.DataFrame(data=world_list)
        worlds_id = worlds_df[worlds_df['name'] == query]['world_id'].item()

        main = Highscores.objects.filter(
            Q(date__gt=date)
            & ~Q(exp_diff=0)
            & Q(world_id=worlds_id)
        ).order_by(
            '-exp_diff'
        )

    content = {
        'main': main,
        'world': query,
        'world_list': world_list
    }

    return render(request, "sites/experience/mainland.html", content)


def rookgaard(request, *args, **kwargs):

    # now = datetime.datetime.now()
    # date = (now - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    date = '2022-12-23 11:11:50'

    top = Highscores.objects.filter(
        Q(date__gt=date)
        & Q(exp_diff__gt=0)
        & Q(voc=1)
    ).order_by(
        '-exp_diff'
    )

    content = {
        'top': top
    }

    return render(request, "sites/experience/rookgaard.html", content)


# Search character
def search_character(request, *args, **kwargs):

    database = True
    # check if it's not empty
    if request.GET:
        query = request.GET['q']  # <input name="q"> return dictionary { q : item }

        # check if it's only characters
        if query.replace(' ', '').isalpha():
            character_information = dataapi.get_character_info(query)

            # check if exist on tibia.com
            if character_information['character']['name'] != '':
                exist = True
            else:
                character_information = f'Character {query} does not exist.'  # if not exist
                exist = False

        else:
            character_information = f'Character {query} does not exist.'  # if contains numbers or special characters
            exist = False

        # if there is no data from search request
    else:
        character_information = ''
        exist = False

    content = {
        'exist': exist,
        'database': database,
        'char': character_information,
    }
    return render(request, "sites/characters/search_character.html", content)


# Discords
def discord(request, *args, **kwargs):
    return render(request, "sites/discords.html")


# About
def about(request, *args, **kwargs):
    return render(request, "sites/about.html")



