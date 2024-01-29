from pathlib import Path
from urllib.parse import urlparse

import scrapy
from scrapy.crawler import CrawlerProcess
import logging

logging.getLogger('scrapy').setLevel(logging.WARNING)
logging.getLogger('scrapy').propagate = False

from luanfunc import download_video, validateTitle


class MySpider(scrapy.Spider):
    name = 'aznude_spider'
    cat = 'realsex'
    start_urls = [f'https://www.aznude.com/tags/vids/{cat}/1.html']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

    def parse(self, response):
        page_number = response.css('div.lbtn-group a:nth-last-child(2)::attr("href")').get()
        page_number = int(page_number.split('/')[-1].split('.')[0])
        page_number = 30
        print(f"找到{page_number}页数据.")
        for index in range(25, int(page_number) + 1):
            request = scrapy.Request(url=f'https://www.aznude.com/tags/vids/{self.cat}/{index}.html',
                                     callback=self.get_pages)
            request.cb_kwargs["index"] = index
            yield request

    def get_pages(self, response, index):
        urls = response.css('div.movie a::attr("href")').getall()
        print(f"第{index}页，找到{len(urls)}个视频")
        for video_index, url in enumerate(urls):
            request = scrapy.Request(url=f"https://www.aznude.com{url}", callback=self.get_video)
            request.cb_kwargs["index"] = index
            request.cb_kwargs["video_index"] = video_index
            yield request

    def get_video(self, response, index, video_index):
        video = response.css('ul.sorting-buttons a:nth-child(3)::attr("href")').get()
        name1 = response.css('h2 span a::text').getall()[0]
        name2 = response.css('h2::text').get()
        name3 = response.css('h2 a::text').getall()[1]
        name = f"{name1}{name2}{name3}"
        parsed_url = urlparse(response.url)
        name2 = parsed_url.path.split('/')[-1].split('.')[0]
        name = f"{validateTitle(name)} [{name2}].mp4"
        file = Path(r"N:\PornVideo\[aznude.com]") / name

        if not file.exists():
            if download_video(f"https:{video}", response.url, file):
                print(f"第{index}页 第{video_index + 1}个视频 {name} 下载成功")
            else:
                print(f"第{index}页 第{video_index + 1}个视频 {name} 下载失败")
                file.unlink()
        else:
            print(f"第{index}页 第{video_index + 1}个视频 {name} 已存在")


process = CrawlerProcess(settings={
    'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7',
})
process.crawl(MySpider)
process.start()
