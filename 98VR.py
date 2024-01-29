from pathlib import Path

import requests
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy import signals
from scrapy.signalmanager import dispatcher
from urllib.parse import urlparse, parse_qs

from luanfunc import download_video, validateTitle

import logging

logging.getLogger('scrapy').setLevel(logging.WARNING)
logging.getLogger('scrapy').propagate = False

logging.FileHandler('example.log')


class MySpider(scrapy.Spider):
    name = '98VR_spider'
    start_urls = ['https://www.sehuatang.net/forum-160-1.html']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    cookies = {}
    image_list = []
    info_list = []
    cookie_list = [
        {
            "domain": ".sehuatang.net",
            "expirationDate": 1733580540.564124,
            "hostOnly": False,
            "httpOnly": True,
            "name": "cf_clearance",
            "path": "/",
            "sameSite": "no_restriction",
            "secure": True,
            "session": False,
            "storeId": "0",
            "value": "TjpgUs39mu6BaND0Hg59ELlLjtfHaOsMIXs4_PYtUGI-1702044540-0-1-9af72544.9c110299.cdf67aa4-0.2.1702044540",
            "id": 1
        },
        {
            "domain": "www.sehuatang.net",
            "expirationDate": 1733580541,
            "hostOnly": True,
            "httpOnly": False,
            "name": "_safe",
            "path": "/",
            "sameSite": "unspecified",
            "secure": False,
            "session": False,
            "storeId": "0",
            "value": "vqd37pjm4p5uodq339yzk6b7jdt6oich",
            "id": 2
        },
        {
            "domain": "www.sehuatang.net",
            "expirationDate": 1704636541.90948,
            "hostOnly": True,
            "httpOnly": False,
            "name": "cPNj_2132_atarget",
            "path": "/",
            "sameSite": "unspecified",
            "secure": True,
            "session": False,
            "storeId": "0",
            "value": "1",
            "id": 3
        },
        {
            "domain": "www.sehuatang.net",
            "expirationDate": 1702649341.909487,
            "hostOnly": True,
            "httpOnly": False,
            "name": "cPNj_2132_forum_lastvisit",
            "path": "/",
            "sameSite": "unspecified",
            "secure": True,
            "session": False,
            "storeId": "0",
            "value": "D_160_1702044541",
            "id": 4
        },
        {
            "domain": "www.sehuatang.net",
            "expirationDate": 1702130941.909459,
            "hostOnly": True,
            "httpOnly": False,
            "name": "cPNj_2132_lastact",
            "path": "/",
            "sameSite": "unspecified",
            "secure": True,
            "session": False,
            "storeId": "0",
            "value": "1702044541%09forum.php%09forumdisplay",
            "id": 5
        },
        {
            "domain": "www.sehuatang.net",
            "hostOnly": True,
            "httpOnly": False,
            "name": "cPNj_2132_lastfp",
            "path": "/",
            "sameSite": "unspecified",
            "secure": False,
            "session": True,
            "storeId": "0",
            "value": "c86c8dbda157135c7a764506bef70c82",
            "id": 6
        },
        {
            "domain": "www.sehuatang.net",
            "expirationDate": 1704636541.909403,
            "hostOnly": True,
            "httpOnly": False,
            "name": "cPNj_2132_lastvisit",
            "path": "/",
            "sameSite": "unspecified",
            "secure": True,
            "session": False,
            "storeId": "0",
            "value": "1702040941",
            "id": 7
        },
        {
            "domain": "www.sehuatang.net",
            "expirationDate": 1704636540.137914,
            "hostOnly": True,
            "httpOnly": True,
            "name": "cPNj_2132_saltkey",
            "path": "/",
            "sameSite": "unspecified",
            "secure": True,
            "session": False,
            "storeId": "0",
            "value": "Vl3q277q",
            "id": 8
        },
        {
            "domain": "www.sehuatang.net",
            "hostOnly": True,
            "httpOnly": False,
            "name": "cPNj_2132_st_t",
            "path": "/",
            "sameSite": "unspecified",
            "secure": True,
            "session": True,
            "storeId": "0",
            "value": "0%7C1702044541%7Cec6a7ac7543b70460aa187bdf76e3b6e",
            "id": 9
        },
        {
            "domain": "www.sehuatang.net",
            "expirationDate": 1704636541.909499,
            "hostOnly": True,
            "httpOnly": False,
            "name": "cPNj_2132_visitedfid",
            "path": "/",
            "sameSite": "unspecified",
            "secure": True,
            "session": False,
            "storeId": "0",
            "value": "160",
            "id": 10
        }
    ]

    def __init__(self, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)

    def parse(self, response):
        for cookie in self.cookie_list:
            self.cookies[cookie["name"]] = cookie["value"]

        page_number = 900
        print(f"找到{page_number}页数据.")
        for index in range(1, int(page_number) + 1):
            request = scrapy.Request(url=f"https://www.sehuatang.net/forum.php?mod=forumdisplay&fid=95&orderby=dateline&typeid=716&orderby=dateline&typeid=716&filter=author&page={index}", cookies=self.cookies,
                                     callback=self.get_pages)
            request.cb_kwargs["index"] = index
            yield request

    def get_pages(self, response, index):
        urls = response.css("tbody[id^='normalthread_'] tr th a.s::attr(href)").getall()
        titles = response.css("tbody[id^='normalthread_'] tr th a.s::text").getall()
        for index, title in enumerate(titles):
            url = f"https://www.sehuatang.net/{urls[index]}"
            if "VR" in title:
                if "VR转" not in title and "国产VR" not in title:
                    self.info_list.append(f"{title} {url}")
        print(f"找到{len(self.info_list)}个视频")
        # for video_index, url in enumerate(urls):
        #     request = scrapy.Request(url=f"https://www.sehuatang.net/{url}", cookies=self.cookies,
        #                              callback=self.get_video)
        #     request.cb_kwargs["index"] = index
        #     request.cb_kwargs["video_index"] = video_index
        #     yield request

    # def get_video(self, response, index, video_index):
    #     title = response.css("h1.ts span::text").get()
    #     image = response.css('img[aid]::attr(file)').get()
    #     url = response.css('div.blockcode div ol li::text').get()
    #     print(f"{response.url} {title} {image} {url}")
    #     self.image_list.append(image)
    #     self.info_list.append(f"{response.url} {title} {image} {url}")

    def spider_closed(self, spider, reason):
        # with open('vr_image.txt', 'w', encoding='utf-8') as file:
        #     for image in self.image_list:
        #         file.write(f'{image}\n')
        with open('vr_info.txt', 'w', encoding='utf-8') as file:
            for info in self.info_list:
                file.write(f'{info}\n')


settings = scrapy.settings.Settings()
settings.set('REQUEST_FINGERPRINTER_IMPLEMENTATION', '2.7')

process = CrawlerProcess(settings)
process.crawl(MySpider)
process.start()
