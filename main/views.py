from django.shortcuts import render
from .models import News, Boosted


# Main page
def main_page(request, *args, **kwargs):
    # news ticker
    latest_tickers = News.objects.filter(type='ticker').order_by('-news_id')[:3]

    # boosted boss
    boosted_boss = Boosted.objects.filter(type='boss').order_by('-boosted_id')[:1]

    # boosted creature
    boosted_creature = Boosted.objects.filter(type='creature').order_by('-boosted_id')[:1]

    content = {
        'news_ticker': latest_tickers,
        'boosted_boss': boosted_boss,
        'boosted_creature': boosted_creature,
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


# About
def about(request, *args, **kwargs):
    return render(request, "sites/about.html")


# Discords
def discord(request, *args, **kwargs):
    return render(request, "sites/discords.html")
