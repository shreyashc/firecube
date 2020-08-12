from django.shortcuts import render
import lxml
from django.http import Http404,HttpResponse,HttpResponseRedirect
from bs4 import BeautifulSoup
import requests
from django.template.defaultfilters import filesizeformat
import pafy
import datetime
def home(request):
	return render(request,'index.html')



def movies(request):
	
	urlOfTrending="https://www.imdb.com/india/released/"

	
	requestOfTrending=requests.get(urlOfTrending)
	

	soupOfTrending=BeautifulSoup(requestOfTrending.content,'lxml')
	rawListOfTrending=soupOfTrending.find_all('div',{"class":"trending-list-rank-item-data-container"})
		
	finalTrendingList=[]

	for trend in rawListOfTrending:
		temp=trend.text.strip().split("\n")
		finalTrendingList.append(temp)

	urlOfTrendingGlobal="https://www.imdb.com/india/global/"

	try:
		requestOfTrendingGlobal=requests.get(urlOfTrendingGlobal)
	except:
		return HttpResponse("Server Error")

	soupOfTrendingGlobal=BeautifulSoup(requestOfTrendingGlobal.content,'lxml')
	rawListOfTrendingGlobal=soupOfTrendingGlobal.find_all('div',{"class":"trending-list-rank-item-data-container"})
		
	finalTrendingListGlobal=[]

	for trend in rawListOfTrendingGlobal:
		temp=trend.text.strip().split("\n")
		finalTrendingListGlobal.append(temp)

	date=datetime.date.today()
	context={
		'list_name':"Trending Movies/Web Series(LOCAL)",
		'movie_list':finalTrendingList,
		'date':date,
		'global_list':finalTrendingListGlobal,
		'global_name':"Trending Movies/Web Series(GLOBAL)"
	}

	return render(request, 'movies.html',context)


def topten(request):

	urlOfBB200="https://www.billboard.com/charts/billboard-200"

	try:
		requestOfBB200=requests.get(urlOfBB200)
	except:
		return HttpResponse("Server error")

	soupOfBB200=BeautifulSoup(requestOfBB200.content,'lxml')

	rawListOfBB200=soupOfBB200.find_all('span',{"class":"chart-element__information"})
	week=soupOfBB200.find('button',{"class":"date-selector__button button--link"})
	current_week=week.text.strip()
	finalBB200List=[]
	i=1
	for song in rawListOfBB200:
		if i>10:
			break
		temp=song.text.strip().split("\n")
		temp[2]=i
		finalBB200List.append(temp)
		i = i+1


	context={

		'song_list':finalBB200List,
		'week':current_week,
		'list_name':"billboard Top 10 Songs"
	}

	return render(request, 'topten.html',context)


def toptwohundred(request):
	urlOfBB200="https://www.billboard.com/charts/billboard-200"

	try:
		requestOfBB200=requests.get(urlOfBB200)
	except:
		return HttpResponse("Server error")

	soupOfBB200=BeautifulSoup(requestOfBB200.content,'lxml')

	rawListOfBB200=soupOfBB200.find_all('span',{"class":"chart-element__information"})
	week=soupOfBB200.find('button',{"class":"date-selector__button button--link"})
	current_week=week.text.strip()
	finalBB200List=[]
	i=1
	for song in rawListOfBB200:
		if i>200:
			break
		temp=song.text.strip().split("\n")
		temp[2]=i
		finalBB200List.append(temp)
		i = i+1


	context={

		'song_list':finalBB200List,
		'week':current_week,
		'list_name':"billboard Top 200 Songs"
	}

	return render(request, 'toptwohundred.html',context)

def hothundred(request):
	urlOfHot100="https://www.billboard.com/charts/hot-100"

	try:
		requestOfHot100=requests.get(urlOfHot100)
	except:
		return HttpResponse("server error")

	soupOfHot100=BeautifulSoup(requestOfHot100.content,'lxml')
		
	rawListOfHot100=soupOfHot100.find_all('span',{"class":"chart-element__information"})
	week=soupOfHot100.find('button',{"class":"date-selector__button button--link"})
	current_week=week.text.strip()


	finalHot100List=[]
	i=1
	for song in rawListOfHot100:
		if i >100:
			break
		temp=song.text.strip().split("\n")
		temp[2]=i
		finalHot100List.append(temp)
		i = i+1


	context={

		'song_list':finalHot100List,
		'week':current_week,
		'list_name':"billboard hot 100 Songs"
	}

	return render(request, 'hothundred.html',context)


def ytredirect(request):
	video_name=str(request.GET['query'])
	headers= {"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}
	base_url_yt="https://www.youtube.com/"
	url_for_searchquery_request="https://www.youtube.com/results?search_query="+video_name

	try:
		r= requests.get(url_for_searchquery_request,headers=headers)
	except:
		return HttpHttpResponse("Server Error")
		
	try:
		soup=BeautifulSoup(r.content,'lxml')
	except:
		soup=BeautifulSoup(r.content,'html.parser')

	related_url_list=[]

	for url in soup.find_all('a'):
	    if url.get('href')[:7] == '/watch?':
	    	related_url_list.append(url.get('href'))

	try:
		redirect_url = base_url_yt+related_url_list[0]
	except:
		return HttpResponse("Server Busy! Please Try again")
		

		
	return HttpResponseRedirect(redirect_url)

def kannadatopfifty(request):
	url_for_kannada_topfifty_request="https://gaana.com/playlist/gaana-dj-kannada-top-20"

	try:
		r= requests.get(url_for_kannada_topfifty_request)
	except:
		return HttpResponse("Server Error")
	
	try:
		soup=BeautifulSoup(r.content,'lxml')
	except:
		soup=BeautifulSoup(r.content,'html.parser')

	final_song_artist_list=[]
	i=1 
	for div_of_song in soup.find_all('div',{"class":"playlist_thumb_det"}):

		all_anchor_tags_of_each_song = div_of_song.find_all('a')
		
		list_for_each_song = [" "]
		
		for anchor_tags_of_song_artist in all_anchor_tags_of_each_song:
			
			if 'song' in anchor_tags_of_song_artist.get('href'):
				list_for_each_song.append(anchor_tags_of_song_artist.text)
			if 'artist' in anchor_tags_of_song_artist.get('href'):
				list_for_each_song.append(anchor_tags_of_song_artist.text)
			
			
		list_for_each_song[0]=i
		i = i + 1

		final_song_artist_list.append(list_for_each_song)
		date=datetime.date.today()

	context={
		'song_list':final_song_artist_list,
		'list_name':"Kannada Weekly Top 50 Songs",
		'date':date
	}

	return render(request, 'topfifty.html',context)


def hinditopfifty(request):
	url_for_hindi_topfifty_request="https://gaana.com/playlist/gaana-dj-bollywood-top-50-1"

	try:
		r= requests.get(url_for_hindi_topfifty_request)
	except:
		return HttpResponse("Server Error")

	try:
		soup=BeautifulSoup(r.content,'lxml')
	except:
		soup=BeautifulSoup(r.content,'html.parser')
	

	final_song_artist_list=[]
	i=1 
	for div_of_song in soup.find_all('div',{"class":"playlist_thumb_det"}):

		all_anchor_tags_of_each_song = div_of_song.find_all('a')
		
		list_for_each_song = [" "]
		
		for anchor_tags_of_song_artist in all_anchor_tags_of_each_song:
			
			if 'song' in anchor_tags_of_song_artist.get('href'):
				list_for_each_song.append(anchor_tags_of_song_artist.text)
			if 'artist' in anchor_tags_of_song_artist.get('href'):
				list_for_each_song.append(anchor_tags_of_song_artist.text)
			
			
		list_for_each_song[0]=i
		i = i + 1

		final_song_artist_list.append(list_for_each_song)

		date=datetime.date.today()

	context={
		'song_list':final_song_artist_list,
		'list_name':"Hindi Weekly Top 50 Songs",
		'date':date
	}

	return render(request, 'topfifty.html',context)



def download(request):
	video_name=str(request.GET['query'])
	headers= {"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}
	base_url_yt="https://www.youtube.com/"
	url_for_searchquery_request="https://www.youtube.com/results?search_query="+video_name

	try:
		r= requests.get(url_for_searchquery_request,headers=headers)
	except:
		return HttpResponse("Server Error")
	
	try:
		soup=BeautifulSoup(r.content,'lxml')
	except:
		soup=BeautifulSoup(r.content,'html.parser')
	

	related_url_list=[]

	for url in soup.find_all('a'):
	    if url.get('href')[:7] == '/watch?':
	    	related_url_list.append(url.get('href'))
	    	break

	try:
		video_url = base_url_yt+related_url_list[0]
	except:
		return HttpResponse("Server Busy! Please Try again.")

	
	
	pafy.set_api_key('AIzaSyD-owYkNboeFdmz_6W3Wfg9S8HCI-lqZAU')
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

	# stream_video = video.videostreams
	# video_streams = []
	# video_limit=0
	# for s in stream_video:
	# 	if video_limit > 3:
	# 		break
	# 	video_limit = video_limit + 1
	# 	video_streams.append({
	# 	    'resolution': s.resolution,
	# 	    'extension': s.extension,
	# 	    'file_size': filesizeformat(s.get_filesize()),
	# 	    'video_url': s.url + "&title=" + video.title
	# 	})

    
	audio_streams = []
	audio_limit=0
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
            'audio_streams':audio_streams,
            # 'video_streams':video_streams,
            'title': video.title,                       
            'thumb': video.bigthumbhd,                         
        }
	
	return render(request,'download.html',context)



def youtube(request):
	return render(request, 'yt.html')


def ytdownloader(request):

	pafy.set_api_key('AIzaSyD-owYkNboeFdmz_6W3Wfg9S8HCI-lqZAU')
	
	video_url=request.GET['video_url']
	try:
		video = pafy.new(video_url)
	except:
		context={
		'error':"invalid url"
		}
		return render(request, 'yt.html',context)

	
	
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

	stream_video = video.videostreams
	video_streams = []
	for s in stream_video:
	    video_streams.append({
	        'resolution': s.resolution,
	        'extension': s.extension,
	        'file_size': filesizeformat(s.get_filesize()),
	        'video_url': s.url + "&title=" + video.title
	    })

    
	audio_streams = []
	for s in stream_audio:
	    audio_streams.append({
	        'resolution': s.resolution,
	        'extension': s.extension,
	        'file_size': filesizeformat(s.get_filesize()),
	        'video_url': s.url + "&title=" + video.title
	    })

	context = {
            'streams': video_audio_streams,
            'audio_streams':audio_streams,
            'video_streams':video_streams,
            'title': video.title,                       
            'thumb': video.bigthumbhd,                         
        }
	
	return render(request,'download.html',context)


def about(request):
	return render(request, 'about.html')
