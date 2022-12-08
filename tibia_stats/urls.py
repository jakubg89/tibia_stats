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
from main.views \
    import \
    main_page,\
    under_construction,\
    sign_in,\
    sign_up,\
    about, \
    worlds

# Error custom view
handler404 = 'main.views.error404'
# handler500 = 'mysite.views.my_custom_error_view'
# handler403 = 'mysite.views.my_custom_permission_denied_view'
# handler400 = 'mysite.views.my_custom_bad_request_view'

urlpatterns = [

    # Admin
    path('admin/', admin.site.urls),

    # Home page
    path('', main_page),
    path('home/', main_page),

    # Sign in / Sign up
    path('signin/', sign_in),
    path('signup/', sign_up),

    # Experience menu
    path('experience/top500', under_construction),
    path('experience/mainland', under_construction),
    path('experience/rookgaard', under_construction),
    path('experience/stats', under_construction),

    # Charms menu
    path('charms/top500', under_construction),
    path('charms/mainland', under_construction),
    path('charms/rookgaard', under_construction),
    path('charms/stats', under_construction),

    # Char bazaar menu
    path('bazaar/active', under_construction),
    path('bazaar/history', under_construction),
    path('bazaar/stats', under_construction),

    # Worlds menu
    path('worlds/allworlds', worlds),
    path('worlds/world', under_construction),
    path('worlds/online', under_construction),

    # Character menu
    path('character/search', under_construction),
    path('character/transfers', under_construction),
    path('character/name_change', under_construction),

    # Boss menu
    path('bosses/list', under_construction),
    path('bosses/stats', under_construction),

    # Calculators menu
    path('calculator/training', under_construction),
    path('calculator/loot', under_construction),
    path('calculator/stamina', under_construction),

    # Other
    path('discord/', under_construction),
    path('about/', about),
]


