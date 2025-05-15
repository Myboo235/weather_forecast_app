import datetime
import argparse
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", options=chrome_options)


driver.get('https://www.accuweather.com/en/world-weather')

# Get the title of the webpage
page_title = driver.title
print("Page Title:", page_title)

driver.quit()
