"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from myapp import views
from myapp.views import liveMatchSerializer, realTimeSerializer, upcomingFantasyMatchSerializer, fantasyTeamSerializer
from myapp.api import api

urlpatterns = [
    path('admin/', admin.site.urls),

    # API TO START ONE-TIME SCRAPING OF ANY MATCH/FIXTURE
    path(r'api/crex/liveMatch/getdata/', liveMatchSerializer.as_view(), name="get_live_commentary"),

    # API TO START REAL-TIME SCRAPING OF A LIVE MATCH
    path(r'api/crex/realTimeScore', realTimeSerializer.as_view(), name="real_time_score"),

    path(r'api/criclytics/upcomingMatches', upcomingFantasyMatchSerializer.as_view(), name="upcoming_fantasy_matches"),

    path(r'api/crex/fantasyTeam', fantasyTeamSerializer.as_view(), name="fantasy_team"),

    path("api/", api.urls),
]
