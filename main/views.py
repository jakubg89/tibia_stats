from django.shortcuts import render


def main_page(request, *args, **kwargs):
    return render(request, "sites/index.html")
