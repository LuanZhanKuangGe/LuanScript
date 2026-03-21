import json
from pathlib import Path

import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import urlparse, parse_qs

from luanfunc import download_video, validateTitle

class FypptSpider(scrapy.Spider):
    name = 'fyptt_spider'
    start_urls = ['https://allclassic.porn/get_file/1/52c08d22e114e06838fa477ce48fede7f945bab8c2/0/353/353.mp4/?rnd=1729423763434']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

    def parse(self, response):
        print(response)
        pass

if __name__ == "__main__":
    settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7'
    }

    process = CrawlerProcess(settings=settings)
    process.crawl(FypptSpider)
    # process.crawl(OnlytikSpider)
    process.start()
