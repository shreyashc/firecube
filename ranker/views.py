import datetime
import json
import os
import random
import re
from urllib.parse import quote

import lxml
import pafy
import requests
import youtube_dl
from bs4 import BeautifulSoup
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import (Http404, HttpResponse, HttpResponseRedirect,
                         JsonResponse)
from django.shortcuts import redirect, render, reverse
from django.template.defaultfilters import filesizeformat
from django.utils.http import urlencode
from django.views.decorators.csrf import csrf_exempt
from pydub import AudioSegment

from utils import ytscrapper


def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def movies(request):
    urlOfTrending = "https://www.imdb.com/india/released/"

    requestOfTrending = requests.get(urlOfTrending)

    soupOfTrending = BeautifulSoup(requestOfTrending.content, 'lxml')
    rawListOfTrending = soupOfTrending.find_all(
        'div', {"class": "trending-list-rank-item-data-container"})

    finalTrendingList = [
        {
            "title": trend.text.strip().split("\n")[2]
        }
        for trend in rawListOfTrending
    ]

    urlOfTrendingGlobal = "https://www.imdb.com/india/global/"

    try:
        requestOfTrendingGlobal = requests.get(urlOfTrendingGlobal)
    except:
        return HttpResponse("Server Error")

    soupOfTrendingGlobal = BeautifulSoup(
        requestOfTrendingGlobal.content, 'lxml')

    rawListOfTrendingGlobal = soupOfTrendingGlobal.find_all(
        'div', {"class": "trending-list-rank-item-data-container"})

    finalTrendingListGlobal = [
        {
            "title": trend.text.strip().split("\n")[2]
        }
        for trend in rawListOfTrendingGlobal
    ]
    context = {
        'title': "Trending",
        'local_list_name': "Trending Movies/Web Series (India)",
        'local_list': finalTrendingList,
        'global_list_name': "Trending Movies/Web Series(Global)",
        'global_list': finalTrendingListGlobal,
        'week': datetime.date.today(),
    }

    return render(request, 'trending.html', context)


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

    finalBB200List = [
        {"name": song.text.strip().split(
            "\n")[0], "artist":song.text.strip().split("\n")[1]}
        for song in rawListOfBB200[:201]
    ]

    context = {

        'song_list': finalBB200List,
        'week': current_week,
        'list_name': "billboard Top 200 Songs",
        'title': "Billboard 200"
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

    finalHot100List = [
        {"name": song.text.strip().split(
            "\n")[0], "artist":song.text.strip().split("\n")[1]}
        for song in rawListOfHot100[:201]
    ]

    context = {

        'song_list': finalHot100List,
        'week': current_week,
        'list_name': "billboard hot 100 Songs",

    }

    return render(request, 'toptwohundred.html', context)


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

    rawKanSongs = soup.find_all(
        'div', {"class": "playlist_thumb_det"})

    anchors_in_kan_songs = [
        song_div.find_all('a') for song_div in rawKanSongs
    ]

    final_kan_songs = [
        get_formatted_song(anchor_tags)
        for anchor_tags in anchors_in_kan_songs
    ]
    print(final_kan_songs)

    context = {
        'song_list': final_kan_songs,
        'list_name': "Kannada Weekly Top 50 Songs",
        'week': datetime.date.today(),
        'title': 'Kannada Top 50'
    }

    return render(request, 'toptwohundred.html', context)


def hinditopfifty(request):
    url_hindi_topfifty = "https://gaana.com/playlist/gaana-dj-bollywood-top-50-1"

    try:
        response = requests.get(url_hindi_topfifty)
    except:
        return HttpResponse("Server Error")

    try:
        soup = BeautifulSoup(response.content, 'lxml')
    except:
        soup = BeautifulSoup(response.content, 'html.parser')

    date = datetime.date.today()

    rawHindiSongs = soup.find_all(
        'div', {"class": "playlist_thumb_det"})

    anchors_in_hindi_songs = [
        song_div.find_all('a') for song_div in rawHindiSongs
    ]

    final_hindi_songs = [
        get_formatted_song(anchor_tags)
        for anchor_tags in anchors_in_hindi_songs
    ]

    context = {
        'song_list': final_hindi_songs,
        'list_name': "Hindi Weekly Top 50 Songs",
        'week': datetime.date.today(),
        'title': 'Hindi Top 50'
    }

    return render(request, 'toptwohundred.html', context)


def ytredirect(request):
    video_name = str(request.GET['query'])
    redirect_url = ytscrapper.getYtUrl(video_name)
    if redirect_url is None:
        return HttpResponse("Server Busy! Please Try again")
    return HttpResponseRedirect(redirect_url)


def download_from_name(request):
    video_name = str(request.GET['query'])
    video_url = ytscrapper.getYtUrl(video_name)
    if video_url is None:
        return HttpResponse("Could Not Find Video")
    redirect_url = reverse('ytdownloader') + f'?video_url={video_url}'
    return redirect(redirect_url)


def youtube(request):
    return render(request, 'youtube_from.html')


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
        return render(request, 'youtube_from.html', context)

    video_audio_streams = [
        {
            'resolution': s.resolution.split("x")[1]+"p",  # 360p,720p..
            'extension': s.extension,
            'file_size': filesizeformat(s.get_filesize()),
            'video_url': s.url + "&title=" + video.title
        }
        for s in video.streams
    ]

    audio_streams = [
        {
            'bitrate': s.rawbitrate // 1000,  # bps -> kbps
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
            'thumb': video.bigthumbhd.replace("http://", "https://"),
            'duration': video.duration,
            'published': video.published,
            'viewcount': video.viewcount,
            'videoid': video.videoid
        }
    }

    return render(request, 'download.html', context)


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

        if stream_type == 'audio-mp3':
            stream = video.audiostreams[idx]
            _filename = video.title + \
                str(stream.rawbitrate // 1000) + "."+stream.extension
            _filename = normalizeFilename(_filename)
            filepath_temp = os.path.join(settings.MEDIA_ROOT, _filename)
            stream.download(filepath=filepath_temp, quiet=True)
            sound = AudioSegment.from_file(
                os.path.join(settings.MEDIA_ROOT, _filename))
            filepath_temp = os.path.join(
                settings.MEDIA_ROOT, _filename.replace("."+stream.extension, ".mp3"))
            sound.export(filepath_temp, format="mp3",
                         bitrate=str(stream.rawbitrate // 1000)+"K")
            filepath_temp = "/media/" + \
                _filename.replace("."+stream.extension, ".mp3")

        elif stream_type == 'audio':
            stream = video.audiostreams[idx]
            _filename = video.title + \
                str(stream.rawbitrate // 1000) + "."+stream.extension
            _filename = normalizeFilename(_filename)
            filepath_temp = os.path.join(settings.MEDIA_ROOT, _filename)
            stream.download(filepath=filepath_temp, quiet=True)
            filepath_temp = "/media/" + _filename

        elif stream_type == 'video':
            stream = video.streams[idx]
            _filename = video.title + \
                stream.resolution.split("x")[1]+"p" + "." + stream.extension
            _filename = normalizeFilename(_filename)
            filepath_temp = os.path.join(settings.MEDIA_ROOT, _filename)
            stream.download(filepath=filepath_temp, quiet=False)
            filepath_temp = "/media/" + _filename

    except Exception as e:
        print(e)
        return JsonResponse(status=400, data={'message': "could not find video/audio"})

    return JsonResponse({'filepath': filepath_temp})


def normalizeFilename(filename):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_filename = re.sub(rstr, "", filename)
    return new_filename.strip()


def get_formatted_song(anchor_tags):
    formatted_song = {}
    for anchor_tag in anchor_tags:
        if 'song' in anchor_tag.get('href'):
            formatted_song['name'] = anchor_tag.text
        if 'artist' in anchor_tag.get('href'):
            formatted_song['artist'] = anchor_tag.text
    return formatted_song
