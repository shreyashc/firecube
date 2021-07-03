from selenium import webdriver
from bs4 import BeautifulSoup
import os
import lxml
from django.conf import settings

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('headless')
prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2}}
chrome_options.add_experimental_option('prefs', prefs)

if settings.DEBUG:
	browser = webdriver.Chrome(executable_path=os.path.join(settings.BASE_DIR,"webdriver","chromedriver.exe") ,chrome_options=chrome_options)
else:
	CHROMEDRIVER_PATH = "/app/.chromedriver/bin/chromedriver"
	chrome_bin = os.environ.get('GOOGLE_CHROME_BIN', "chromedriver")
	chrome_options.binary_location = chrome_bin
	browser = webdriver.Chrome(
    executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
    #heroku stuff


def getYtUrl(video_title):
	browser.get('https://www.youtube.com/results?search_query='+video_title)
	html = browser.page_source
	soup = BeautifulSoup(html, 'lxml')
	video_url = None

	for url in soup.find_all('a'):
		if(url.get('href') != None):
			if(url.get('href')[:7] == '/watch?'):
				video_url = url.get('href')
				break
	if(video_url is not None):
		return "https://www.youtube.com" + video_url
	return video_url

