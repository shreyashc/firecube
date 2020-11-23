import os
from selenium import webdriver
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
web_dirver_path = os.path.join(BASE_DIR, '..', 'webdriver', 'chromedriver.exe')

op = webdriver.ChromeOptions()
op.add_argument('headless')

driver = webdriver.Chrome(web_dirver_path, options=op)
