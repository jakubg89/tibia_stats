"""tibia_stats URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main.views import (
    main_page,
    under_construction,
    sign_in,
    sign_up,
    about,
    worlds_main,
    single_world,
    search_character,
    top_500,
    mainland,
    rookgaard,
    explore_highscores,
    world_transfers,
    name_changes,
    top_250_charms,
    world_charms,
    kill_stats_main_page
)
from django.conf import settings
from django.conf.urls.static import static

# Error custom view
handler404 = "main.views.error404"
handler500 = "main.views.error500"
handler403 = "main.views.error403"
handler400 = "main.views.error400"

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # Home page
    path("", main_page),
    path("home/", main_page),
    # Sign in / Sign up
    path("signin/", sign_in),
    path("signup/", sign_up),
    # Experience menu
    path("experience/top500", top_500),
    path("experience/mainland/", mainland),
    path("experience/rookgaard", rookgaard),
    path("experience/explore/", explore_highscores),
    path("experience/stats", under_construction),
    # Charms menu
    path("charms/top250", top_250_charms),
    path("charms/world-charms/", world_charms),
    # path("charms/rookgaard", under_construction),
    path("charms/stats", under_construction),
    # Char bazaar menu
    path("bazaar/active", under_construction),
    path("bazaar/history", under_construction),
    path("bazaar/stats", under_construction),
    # Worlds menu
    path("worlds/allworlds", worlds_main),
    path("worlds/world/<str:name>/", single_world),
    path("worlds/online", under_construction),
    # Character menu
    path("character/search/", search_character),
    path("character/transfers", world_transfers),
    path("character/name_change", name_changes),
    # Boss menu
    path("kill-stats/monsters/", kill_stats_main_page),
    path("kill-stats/bosses/", under_construction),
    # Calculators menu
    path("calculator/training", under_construction),
    path("calculator/loot", under_construction),
    path("calculator/stamina", under_construction),
    # Other
    path("discord/", under_construction),
    path("about/", about),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
