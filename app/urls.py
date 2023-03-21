from django.urls import path
from app.views import *

urlpatterns = [
    path('', homePage,name='homePage'),
    path('about/', aboutPage,name='aboutPage'),
    path('summoner/<region>/<summoner_name>/', summonerPage,name='summonerPage'),
    # path('iha/add/', ihaAddPage,name='ihaAddPage'),
    # path('iha/list/', ihaListPage,name='ihaListPage'),
    # path('iha/update/<id>/', ihaUpdatePage,name='ihaUpdatePage'),
]