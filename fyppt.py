import json
from pathlib import Path

import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import urlparse, parse_qs

from luanfunc import download_video, validateTitle

import logging

logging.getLogger('scrapy').setLevel(logging.WARNING)
logging.getLogger('scrapy').propagate = False


class FypptSpider(scrapy.Spider):
    name = 'fyptt_spider'
    start_urls = ['https://fyptt.to']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

    def parse(self, response):
        page_number = response.css('ul.page-numbers li:nth-last-child(2) a::text').get()
        page_number = 5
        print(f"找到{page_number}页数据.")
        for index in range(1, int(page_number) + 1):
            request = scrapy.Request(url=f"https://fyptt.to/page/{index}", callback=self.get_pages)
            request.cb_kwargs["index"] = index
            yield request

    def get_pages(self, response, index):
        urls = response.css("h3.fl-post-grid-title a::attr('href')").getall()
        print(f"第{index}页，找到{len(urls)}个视频")
        for video_index, url in enumerate(urls):
            request = scrapy.Request(url=url, callback=self.get_video)
            request.cb_kwargs["index"] = index
            request.cb_kwargs["video_index"] = video_index
            yield request

    @staticmethod
    def get_video(response, index, video_index):
        parsed_url = urlparse(response.url)
        id = parsed_url.path.split('/')[1]
        title = parsed_url.path.split('/')[2]
        name = f"[{id}]{title}"
        name = validateTitle(name)
        name = f"{name}.mp4"

        parsed_url = urlparse(response.css("iframe::attr(src)").get())
        params = parse_qs(parsed_url.query)
        video = f"{params['fileid'][0]}.mp4"

        file = Path(r"V:\【fyptt】") / name
        if not file.exists():
            if download_video(f"https://stream.fyptt.to/{video}", response.url, file):
                print(f"第{index}页 第{video_index + 1}个视频 {name} 下载成功")
            else:
                print(f"第{index}页 第{video_index + 1}个视频 {name} 下载失败")
                file.unlink()
        else:
            print(f"第{index}页 第{video_index + 1}个视频 {name} 已存在")


class OnlytikSpider(scrapy.Spider):
    name = 'onlytik_spider'
    start_urls = ['https://onlytik.com/@onlytik']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

    def parse(self, response):
        start_page = 0
        page_number = 10
        for index in range(start_page, start_page + int(page_number) + 1):
            request = scrapy.Request(url=f"https://onlytik.com/api/user?id=onlytik&offset={index * 10}",
                                     callback=self.get_video)
            yield request

    @staticmethod
    def get_video(response):
        data_dict = json.loads(response.text)
        for video in data_dict['videos']:
            url = video['url']
            name = url.split('/')[-1]
            file = Path(r"V:\【onlytik】") / name
            if not file.exists():
                if download_video(url, response.url, file):
                    print(f"{url} 下载成功")
                else:
                    print(f"{url} 下载失败")
                    file.unlink()
            else:
                print(f"{url} 已存在")


if __name__ == "__main__":
    settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7'
    }

    process = CrawlerProcess(settings=settings)
    process.crawl(FypptSpider)
    process.crawl(OnlytikSpider)
    process.start()
