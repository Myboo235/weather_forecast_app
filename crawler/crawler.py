#!/usr/bin/env python3
import argparse
import datetime
import logging
import urllib.robotparser
import pandas as pd
import os
import pytz

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    WebDriverException, NoSuchElementException, TimeoutException
)

VIETNAM_TZ = pytz.timezone('Asia/Ho_Chi_Minh')
CURRENT_DATE = datetime.datetime.now(VIETNAM_TZ).date()
CURRENT_HOUR = int(datetime.datetime.now(VIETNAM_TZ).hour)

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def parse_args():
    parser = argparse.ArgumentParser(
        description='Scrape historical weather data from worldweatheronline for a specific date.'
    )
    parser.add_argument('--output', type=str, default='weather.csv', help='Output CSV file name')
    parser.add_argument('--date', type=str, default=CURRENT_DATE.strftime('%Y-%m-%d'), help='Date to crawl in YYYY-MM-DD format')
    parser.add_argument('--timestamp', type=str, default=None, help='timestamp to crawl: 00:00, 03:00, 06:00, 09:00, 12:00, 15:00, 18:00, 21:00')
    return parser.parse_args()

def main():
    args = parse_args()
    url = 'https://www.worldweatheronline.com/da-nang-weather-history/vn.aspx'
    weather_timestamps = [
        "00:00", "03:00", "06:00", "09:00", "12:00", "15:00", "18:00", "21:00"
    ]
    filtered_timestamps = []
    is_current_date = False

    os.system('cls' if os.name == 'nt' else 'clear')
    setup_logging()

    # Validate and convert date
    try:
        crawl_date = datetime.datetime.strptime(args.date, '%Y-%m-%d')
        is_current_date = crawl_date.date() == CURRENT_DATE
    except ValueError as e:
        logging.error(f"Invalid date format: {e}")
        return

    # Filter timestamp before current time
    if is_current_date:
        filtered_timestamps = [timestamp for timestamp in weather_timestamps if int(timestamp[:2]) <= CURRENT_HOUR]
        url = "https://www.worldweatheronline.com/da-nang-weather/vn.aspx?day=20&tp=1"
    else:
        filtered_timestamps = weather_timestamps


    # Thêm log sau khi lọc timestamp
    logging.info(f"Vietnam time now: {CURRENT_DATE}")
    logging.info(f"Filtered timestamps: {filtered_timestamps}")

    if args.timestamp:
        if args.timestamp not in filtered_timestamps:
            logging.error(f"Timestamp {args.timestamp} is not in the filter list.")
            return
        filtered_timestamps = [args.timestamp]
    else:
        logging.info("No timestamp provided. Crawl all timestamps")

    # Check robots.txt permission
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url('https://www.worldweatheronline.com/robots.txt')
    rp.read()
    if not rp.can_fetch('*', url):
        logging.error("Fetching is disallowed by robots.txt")
        return
    logging.info("Check robots.txt permission ✅")
    

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    # Instantiate the Selenium Chrome driver directly
    # browser = webdriver.Remote("http://127.0.0.1:4444/wd/hub", options=chrome_options)
    browser = webdriver.Chrome(options=chrome_options) # local
    browser.get(url)
    wait = WebDriverWait(browser, 10)
    logging.info("Instantiate the Selenium Chrome driver directly ✅")

    columns_name = [
        'Date',
        'Time',
        'Weather',
        'Temp',
        'Rain',
        'Cloud',
        'Pressure',
        'Wind',
        'Gust',
    ]
    results = [columns_name]

    date_str = crawl_date.strftime('%Y-%m-%d')
    logging.info(f"Processing date: {date_str} ⌛")

    if is_current_date:
        try:
            # Wait for the date header to load
            date_header = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.days-collapse-date')))
            date_col = date_header.text.strip() + ' ' + str(crawl_date.year)
        except TimeoutException:
            logging.error(f"Timeout waiting for date header on {date_str} ⚠️")
            browser.quit()
            return
        
        try:
            # Wait for data rows to load
            rows = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'tr.days-details-row1.text-center')))
        except TimeoutException:
            logging.error(f"No data rows found for {date_str} ⚠️")
            browser.quit()
            return
        
        for i in range(0, 8):
            row = rows[i*3+1]
            try:
                cells = row.find_elements(By.TAG_NAME, 'td')
                time_data = cells[0].find_element(By.TAG_NAME, 'p').text.strip()
                if time_data in filtered_timestamps:
                    weather = cells[1].find_element(By.TAG_NAME, 'img').get_attribute('title').strip()
                    temp = cells[2].find_element(By.CLASS_NAME, 'days-table-forecast-p1').text.replace('\n', ' ').strip()
                    rain = cells[3].find_element(By.CLASS_NAME, 'days-rain-number').text.replace('\n', ' ').strip()
                    cloud = cells[4].find_element(By.TAG_NAME, 'p').text.strip()
                    pressure = cells[5].find_element(By.TAG_NAME, 'p').text.strip()
                    wind_speed = cells[6].find_element(By.TAG_NAME, 'div').text.strip()
                    gust = cells[7].find_element(By.TAG_NAME, 'div').text.strip()

                    results.append([date_col,time_data, weather, temp, rain, cloud, pressure, wind_speed, gust])
            except (NoSuchElementException, IndexError) as e:
                logging.error(f"Error processing row: {e} ❗")
                continue
    else:
        try:
            # Set date input and submit form
            input_date = wait.until(EC.presence_of_element_located((By.ID, 'ctl00_MainContentHolder_txtPastDate')))
            browser.execute_script("arguments[0].value = arguments[1];", input_date, date_str)
            submit_date = wait.until(EC.element_to_be_clickable((By.ID, 'ctl00_MainContentHolder_butShowPastWeather')))
            browser.execute_script("arguments[0].click();", submit_date)
        except (WebDriverException, TimeoutException) as e:
            logging.error(f"Error setting date {date_str}: {e} ⚠️")
            browser.quit()
            return

        try:
            # Wait for the date header to load
            date_header = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.days-collapse-date')))
            date_col = date_header.text.strip() + ' ' + str(crawl_date.year)
        except TimeoutException:
            logging.error(f"Timeout waiting for date header on {date_str} ⚠️")
            browser.quit()
            return

        try:
            # Wait for data rows to load
            rows = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'tr.days-details-row1.text-center')))
        except TimeoutException:
            logging.error(f"No data rows found for {date_str} ⚠️")
            browser.quit()
            return

        # Process first 8 rows (skipping header row if needed)
        for row in rows[1:9]:
            try:
                cells = row.find_elements(By.TAG_NAME, 'td')
                time_data = cells[0].find_element(By.TAG_NAME, 'p').text.strip()
                weather = cells[1].find_element(By.TAG_NAME, 'img').get_attribute('title').strip()
                temp = cells[2].find_element(By.CLASS_NAME, 'days-table-forecast-p1').text.replace('\n', ' ').strip()
                rain = cells[3].find_element(By.CLASS_NAME, 'days-rain-number').text.replace('\n', ' ').strip()
                cloud = cells[4].find_element(By.TAG_NAME, 'p').text.strip()
                pressure = cells[5].find_element(By.TAG_NAME, 'p').text.strip()
                wind_speed = cells[6].find_element(By.TAG_NAME, 'div').text.strip()
                gust = cells[7].find_element(By.TAG_NAME, 'div').text.strip()

                results.append([date_col,time_data, weather, temp, rain, cloud, pressure, wind_speed, gust])
            except (NoSuchElementException, IndexError) as e:
                logging.error(f"Error processing row: {e} ❗")
                continue

    browser.quit()
    df = pd.DataFrame(results[1:], columns=results[0])
    df.to_csv(args.output, index=False)
    logging.info(f"Data saved to {args.output} 🚀")

if __name__ == '__main__':
    main()
