from django.shortcuts import render
from .models import News


# Main page
def main_page(request, *args, **kwargs):
    # news ticker
    latest_tickers = News.objects.filter(type='ticker').order_by('-news_id')[:3]
    content = {
        'news_ticker': latest_tickers
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
