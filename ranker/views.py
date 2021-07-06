from django.shortcuts import render
import lxml
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from bs4 import BeautifulSoup
import requests
from django.template.defaultfilters import filesizeformat
import pafy
import datetime
from django.conf import settings
from utils import ytscrapper
import youtube_dl
import json
import random
from django.core.files.storage import FileSystemStorage
from urllib.parse import quote
from pydub import AudioSegment
from django.views.decorators.csrf import csrf_exempt
import os

def home(request):
    return render(request, 'index.html')


def movies(request):
    urlOfTrending = "https://www.imdb.com/india/released/"

    requestOfTrending = requests.get(urlOfTrending)

    soupOfTrending = BeautifulSoup(requestOfTrending.content, 'lxml')
    rawListOfTrending = soupOfTrending.find_all(
        'div', {"class": "trending-list-rank-item-data-container"})

    finalTrendingList = []

    for trend in rawListOfTrending:
        temp = trend.text.strip().split("\n")
        finalTrendingList.append(temp)

    urlOfTrendingGlobal = "https://www.imdb.com/india/global/"

    try:
        requestOfTrendingGlobal = requests.get(urlOfTrendingGlobal)
    except:
        return HttpResponse("Server Error")

    soupOfTrendingGlobal = BeautifulSoup(
        requestOfTrendingGlobal.content, 'lxml')
    rawListOfTrendingGlobal = soupOfTrendingGlobal.find_all(
        'div', {"class": "trending-list-rank-item-data-container"})

    finalTrendingListGlobal = []

    for trend in rawListOfTrendingGlobal:
        temp = trend.text.strip().split("\n")
        finalTrendingListGlobal.append(temp)

    date = datetime.date.today()
    context = {
        'list_name': "Trending Movies/Web Series(LOCAL)",
        'movie_list': finalTrendingList,
        'date': date,
        'global_list': finalTrendingListGlobal,
        'global_name': "Trending Movies/Web Series(GLOBAL)"
    }

    return render(request, 'movies.html', context)


def topten(request):

    urlOfBB200 = "https://www.billboard.com/charts/billboard-200"

    try:
        requestOfBB200 = requests.get(urlOfBB200)
    except:
        return HttpResponse("Server error")

    soupOfBB200 = BeautifulSoup(requestOfBB200.content, 'lxml')

    rawListOfBB200 = soupOfBB200.find_all(
        'span', {"class": "chart-element__information"})
    week = soupOfBB200.find(
        'button', {"class": "date-selector__button button--link"})
    current_week = week.text.strip()
    finalBB200List = []
    i = 1
    for song in rawListOfBB200:
        if i > 10:
            break
        temp = song.text.strip().split("\n")
        temp[2] = i
        finalBB200List.append(temp)
        i = i+1

    context = {

        'song_list': finalBB200List,
        'week': current_week,
        'list_name': "billboard Top 10 Songs"
    }

    return render(request, 'topten.html', context)


def toptwohundred(request):
    urlOfBB200 = "https://www.billboard.com/charts/billboard-200"

    try:
        requestOfBB200 = requests.get(urlOfBB200)
    except:
        return HttpResponse("Server error")

    soupOfBB200 = BeautifulSoup(requestOfBB200.content, 'lxml')

    rawListOfBB200 = soupOfBB200.find_all(
        'span', {"class": "chart-element__information"})
    week = soupOfBB200.find(
        'button', {"class": "date-selector__button button--link"})
    current_week = week.text.strip()
    finalBB200List = []
    i = 1
    for song in rawListOfBB200:
        if i > 200:
            break
        temp = song.text.strip().split("\n")
        temp[2] = i
        finalBB200List.append(temp)
        i = i+1

    context = {

        'song_list': finalBB200List,
        'week': current_week,
        'list_name': "billboard Top 200 Songs"
    }

    return render(request, 'toptwohundred.html', context)


def hothundred(request):
    urlOfHot100 = "https://www.billboard.com/charts/hot-100"

    try:
        requestOfHot100 = requests.get(urlOfHot100)
    except:
        return HttpResponse("server error")

    soupOfHot100 = BeautifulSoup(requestOfHot100.content, 'lxml')

    rawListOfHot100 = soupOfHot100.find_all(
        'span', {"class": "chart-element__information"})
    week = soupOfHot100.find(
        'button', {"class": "date-selector__button button--link"})
    current_week = week.text.strip()

    finalHot100List = []
    i = 1
    for song in rawListOfHot100:
        if i > 100:
            break
        temp = song.text.strip().split("\n")
        temp[2] = i
        finalHot100List.append(temp)
        i = i+1

    context = {

        'song_list': finalHot100List,
        'week': current_week,
        'list_name': "billboard hot 100 Songs"
    }

    return render(request, 'hothundred.html', context)


def ytredirect(request):
    video_name = str(request.GET['query'])
    redirect_url = ytscrapper.getYtUrl(video_name)
    if redirect_url is None:
        return HttpResponse("Server Busy! Please Try again")
    return HttpResponseRedirect(redirect_url)


def kannadatopfifty(request):
    url_for_kannada_topfifty_request = "https://gaana.com/playlist/gaana-dj-kannada-top-20"

    try:
        r = requests.get(url_for_kannada_topfifty_request)
    except:
        return HttpResponse("Server Error")

    try:
        soup = BeautifulSoup(r.content, 'lxml')
    except:
        soup = BeautifulSoup(r.content, 'html.parser')

    final_song_artist_list = []
    i = 1
    for div_of_song in soup.find_all('div', {"class": "playlist_thumb_det"}):

        all_anchor_tags_of_each_song = div_of_song.find_all('a')

        list_for_each_song = [" "]

        for anchor_tags_of_song_artist in all_anchor_tags_of_each_song:

            if 'song' in anchor_tags_of_song_artist.get('href'):
                list_for_each_song.append(anchor_tags_of_song_artist.text)
            if 'artist' in anchor_tags_of_song_artist.get('href'):
                list_for_each_song.append(anchor_tags_of_song_artist.text)

        list_for_each_song[0] = i
        i = i + 1

        final_song_artist_list.append(list_for_each_song)
        date = datetime.date.today()

    context = {
        'song_list': final_song_artist_list,
        'list_name': "Kannada Weekly Top 50 Songs",
        'date': date
    }

    return render(request, 'topfifty.html', context)


def hinditopfifty(request):
    url_for_hindi_topfifty_request = "https://gaana.com/playlist/gaana-dj-bollywood-top-50-1"

    try:
        r = requests.get(url_for_hindi_topfifty_request)
    except:
        return HttpResponse("Server Error")

    try:
        soup = BeautifulSoup(r.content, 'lxml')
    except:
        soup = BeautifulSoup(r.content, 'html.parser')

    final_song_artist_list = []
    i = 1
    for div_of_song in soup.find_all('div', {"class": "playlist_thumb_det"}):

        all_anchor_tags_of_each_song = div_of_song.find_all('a')

        list_for_each_song = [" "]

        for anchor_tags_of_song_artist in all_anchor_tags_of_each_song:

            if 'song' in anchor_tags_of_song_artist.get('href'):
                list_for_each_song.append(anchor_tags_of_song_artist.text)
            if 'artist' in anchor_tags_of_song_artist.get('href'):
                list_for_each_song.append(anchor_tags_of_song_artist.text)

        list_for_each_song[0] = i
        i = i + 1

        final_song_artist_list.append(list_for_each_song)

        date = datetime.date.today()

    context = {
        'song_list': final_song_artist_list,
        'list_name': "Hindi Weekly Top 50 Songs",
        'date': date
    }

    return render(request, 'topfifty.html', context)


def download(request):
    video_name = str(request.GET['query'])
    video_url = ytscrapper.getYtUrl(video_name)
    print(video_url)
    if video_url is None:
        return HttpResponse("Server Busy! Please Try again.")
    ytApiKey = settings.YT_API_KEY
    pafy.set_api_key(ytApiKey)
    video = pafy.new(video_url)
    stream = video.streams
    stream_audio = video.audiostreams
    video_audio_streams = []
    for s in stream:
        video_audio_streams.append({
            'resolution': s.resolution,
            'extension': s.extension,
            'file_size': filesizeformat(s.get_filesize()),
            'video_url': s.url + "&title=" + video.title
        })

    audio_streams = []
    audio_limit = 0
    for s in stream_audio:
        if audio_limit > 3:
            break
        audio_limit = audio_limit + 1
        audio_streams.append({
            'resolution': s.resolution,
            'extension': s.extension,
            'file_size': filesizeformat(s.get_filesize()),
            'video_url': s.url + "&title=" + video.title
        })

    context = {
        'streams': video_audio_streams,
        'audio_streams': audio_streams,
        # 'video_streams':video_streams,
        'title': video.title,
        'thumb': video.bigthumbhd,
    }

    return render(request, 'download.html', context)


def youtube(request):
    return render(request, 'yt.html')


def ytdownloader(request):

    ytApiKey = settings.YT_API_KEY
    pafy.set_api_key(ytApiKey)
    video_url = request.GET['video_url']
    
    try:
        video = pafy.new(video_url)
    except:
        context = {
            'error': "invalid url"
        }
        return render(request, 'yt.html', context)


    video_audio_streams = [
        {
            'resolution': s.resolution.split("x")[1]+"p", # 360p,720p..
            'extension': s.extension,
            'file_size': filesizeformat(s.get_filesize()),
            'video_url': s.url + "&title=" + video.title
        }
        for s in video.streams
        ]
   


    audio_streams = [
        {
            'bitrate': s.rawbitrate // 1000, #bps -> kbps
            'extension': s.extension,
            'file_size': filesizeformat(s.get_filesize()),
            'video_url': s.url + "&title=" + video.title
        }
        for s in video.audiostreams
        ]


    context = {
        'streams': video_audio_streams,
        'audio_streams': audio_streams,
        'meta': {
         'title': video.title,
         'thumb': video.bigthumbhd.replace("http://","https://"),
         'duration':video.duration,
         'published':video.published,
         'viewcount':video.viewcount,
         'videoid':video.videoid
        }
    }

    return render(request, 'download.html', context)


def about(request):
    return render(request, 'about.html')

@csrf_exempt
def get_download_url(request):
    ytApiKey = settings.YT_API_KEY
    pafy.set_api_key(ytApiKey)

    data = request.body.decode('utf-8')
    req_data = json.loads(data)
    videoid = req_data['videoid']
    idx = int(req_data['idx'])
    stream_type = req_data['stream_type']
    
    try:
        video = pafy.new(videoid)

        if stream_type == 'mp3':
            stream = video.audiostreams[idx]
            _filename = video.title+ str(stream.rawbitrate // 1000) +"."+stream.extension
            filepath_temp = os.path.join(settings.MEDIA_ROOT,_filename)
            stream.download(filepath=filepath_temp,quiet=True)
            sound = AudioSegment.from_file(os.path.join(settings.MEDIA_ROOT, _filename))
            filepath_temp = os.path.join(settings.MEDIA_ROOT, _filename.replace("."+stream.extension,".mp3"))
            sound.export(filepath_temp, format="mp3", bitrate = str(stream.rawbitrate // 1000)+"K")
            filepath_temp = "/media/"+ _filename.replace("."+stream.extension,".mp3")
            
        elif stream_type == 'a':
            stream = video.audiostreams[idx]
            filepath_temp = "/media/"+video.title+ str(stream.rawbitrate // 1000) +"."+stream.extension
            stream.download(filepath=filepath_temp,quiet=True)

        elif stream_type == 'v':
            stream = video.streams[idx]
            _filename = video.title+stream.resolution.split("x")[1]+"p" + "."+ stream.extension
            filepath_temp = os.path.join(settings.MEDIA_ROOT,_filename)
            stream.download(filepath=filepath_temp,quiet=False)
            filepath_temp = "/media/" + _filename
            

    except Exception as e:
        print(e)
        return JsonResponse(status=400,data={'message':"could not find video/audio"})

    return JsonResponse({'filepath':filepath_temp})

