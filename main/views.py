from django.shortcuts import render
from django.db import connection
from .models import News, Boosted, World, WorldOnlineHistory
from datetime import datetime
import datetime
from pathlib import Path
import os
import json
import pandas as pd
import scripts.tibiadata_API.get_data as dataapi

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

    content = {
        'news_ticker': latest_tickers,
        'boosted_boss': boosted_boss,
        'boosted_creature': boosted_creature,
        'latest_news': latest_news,
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


# Discords
def discord(request, *args, **kwargs):
    return render(request, "sites/discords.html")


# About
def about(request, *args, **kwargs):
    return render(request, "sites/about.html")



