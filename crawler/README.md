# 🌦️ Weather Forecast App

## 🕸️ Crawler module

- To crawl a specific date run:
```bash
python3 crawler.py --date 2025-01-01
```
- You can check `--help` for more info
```bash
root@aff80b2310a9:/app# python3 crawler.py --help
usage: crawler.py [-h] [--output OUTPUT] [--date DATE]

Scrape historical weather data from worldweatheronline for a specific date.

options:
  -h, --help       show this help message and exit
  --output OUTPUT  Output CSV file name
  --date DATE      Date to crawl in YYYY-MM-DD format
```
- You also run multiple by like [run_multiple_dates](./run_multiple_dates.sh)
```bash
chmod +x ./run_multiple_dates.sh
```