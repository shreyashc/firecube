import os
from selenium import webdriver
GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('headless')

prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2
                            }}
chrome_options.add_experimental_option('prefs', prefs)
browser = webdriver.Chrome(options=chrome_options)

# chrome_options.binary_location = GOOGLE_CHROME_PATH
# browser = webdriver.Chrome(
#     execution_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
