import json
from pathlib import Path

import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import urlparse, parse_qs

from luanfunc import download_video, validateTitle

import logging

logging.getLogger('scrapy').setLevel(logging.WARNING)
logging.getLogger('scrapy').propagate = False

data = {}


class FypptSpider(scrapy.Spider):
    name = 'hotscope_spider'
    start_urls = ['https://hotscope.tv']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

    def parse(self, response):

        start_page = 40
        stop_page = 50
        for index in range(start_page, stop_page):
            request = scrapy.Request(url=f"https://hotscope.tv/popular?page={index}", callback=self.get_pages)
            request.cb_kwargs["index"] = index
            yield request

    def get_pages(self, response, index):
        urls = response.css("div.MuiGrid-item a::attr('href')").getall()
        for video_index, url in enumerate(urls):
            request = scrapy.Request(url=f"https://hotscope.tv{url}", callback=self.get_video)
            request.cb_kwargs["index"] = index
            request.cb_kwargs["video_index"] = video_index
            yield request

    @staticmethod
    def get_video(response, index, video_index):
        url = response.css('div.MuiBox-root video::attr(src)').get()
        title = response.css('div.MuiBox-root h1::text').get()
        if url and title:
            parsed_url = urlparse(response.url)
            id = parsed_url.path.split('/')[2]
            cat = parsed_url.path.split('/')[1]

            name = f"[{id}][{cat}]{title}"
            name = validateTitle(name)
            name = f"{name}.mp4"

            file = Path(r"V:\【hotscope】") / name
            if not file.exists():
                print(url)
                data[url] = name

            # file = Path(r"V:\【hotscope】") / name
            # if not file.exists():
            #     if download_video(url, response.url, file):
            #         print(f"第{index}页 第{video_index + 1}个视频 {name} 下载成功")
            #     else:
            #         print(f"第{index}页 第{video_index + 1}个视频 {name} 下载失败")
            #         file.unlink()
            # else:
            #     print(f"第{index}页 第{video_index + 1}个视频 {name} 已存在")


if __name__ == "__main__":
    settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7'
    }

    process = CrawlerProcess(settings=settings)
    process.crawl(FypptSpider)
    # process.crawl(OnlytikSpider)
    process.start()

    with open("hotscope.json", "w", encoding="utf8") as fp:
        json.dump(data, fp, ensure_ascii=False)
