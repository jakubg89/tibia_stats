from django.shortcuts import render


def main_page(request, *args, **kwargs):
    return render(request, "sites/index.html")


def error404(request, *args, **kwargs):
    return render(request, "sites/404.html")


def under_construction(request, *args, **kwargs):
    return render(request, "sites/under_construction.html")
