from django.urls import path
from .views import home,movies,topten,toptwohundred,hothundred,ytredirect,download,kannadatopfifty,hinditopfifty,youtube,ytdownloader,about
urlpatterns=[
	path('', home,name='home'),
	path('movies/', movies,name='movies'),
	path('topten', topten,name='topten'),
	path('toptwohundred', toptwohundred,name='toptwohundred'),
	path('hothundred', hothundred,name="hothundred"),
	path('ytredirect', ytredirect,name='ytredirect'),
	path('kannadatopfifty', kannadatopfifty,name='kannadatopfifty'),
	path('hinditopfifty', hinditopfifty,name='hinditopfifty'),
	path('download', download,name='download'),
	path('youtube', youtube,name='youtube'),
	path('ytdownloader', ytdownloader,name='ytdownloader'),
	path('about', about,name='about'),
]