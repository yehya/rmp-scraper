# rmp-scraper

This will scrape all professors in a specified university and dump it into one JSON file.

###Requirements:

* Install [scrapy](http://doc.scrapy.org/en/latest/intro/install.html)

###Usage:

1. Go to *rmp_scraper/spiders/rmp_spider.py* and change the ```university``` variable to the university you want to scrape.
2. In a terminal run:
```$ scrapy crawl rmp_scraper -o output/outputFileName.json```