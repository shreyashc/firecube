from selenium import webdriver
from bs4 import BeautifulSoup
import lxml
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('headless')
# chrome_options.binary_location = GOOGLE_CHROME_PATH
prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2
                            }}
chrome_options.add_experimental_option('prefs', prefs)

chrome_options.binary_location = GOOGLE_CHROME_PATH
browser = webdriver.Chrome(
    execution_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)

# browser = webdriver.Chrome(options=chrome_options)


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

