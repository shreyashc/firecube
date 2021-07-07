from django.urls import path
from .views import home, movies, toptwohundred, hothundred, ytredirect, download_from_name, kannadatopfifty, hinditopfifty, youtube, ytdownloader, about, get_download_url

urlpatterns = [
    path('', home, name='home'),
    path('movies', movies, name='movies'),
    path('toptwohundred', toptwohundred, name='toptwohundred'),
    path('hothundred', hothundred, name="hothundred"),
    path('ytredirect', ytredirect, name='ytredirect'),
    path('kannadatopfifty', kannadatopfifty, name='kannadatopfifty'),
    path('hinditopfifty', hinditopfifty, name='hinditopfifty'),
    path('download_from_name', download_from_name, name='download_from_name'),
    path('youtube', youtube, name='youtube'),
    path('ytdownloader', ytdownloader, name='ytdownloader'),
    path('get_download_url', get_download_url, name='get_download_url'),
    path('about', about, name='about'),
]
