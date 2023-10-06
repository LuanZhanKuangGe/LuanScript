from pathlib import Path

import requests
import scrapy
from tqdm import tqdm
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from urllib.parse import urlparse, parse_qs

import logging

# logging.getLogger('scrapy').setLevel(logging.WARNING)
# logging.getLogger('scrapy').propagate = False


def download_video(url, ref, filename):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Referer': ref,
        'Origin': ref
    }

    response = requests.get(url, stream=True, headers=headers)

    total_size = int(response.headers.get('Content-Length', 0))

    block_size = 1024
    progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)

    with open(filename, 'wb') as f:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            f.write(data)

    progress_bar.close()
    if total_size != 0 and progress_bar.n != total_size:
        return 0
    return 1


class MySpider(scrapy.Spider):
    name = 'aznude_spider'
    cat = 'realsex'
    start_urls = [f'https://www.aznude.com/tags/vids/{cat}/1.html']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

    def parse(self, response):
        page_number = response.css('div.lbtn-group a:nth-last-child(2)::attr("href")').get()
        page_number = int(page_number.split('/')[-1].split('.')[0])
        page_number = 1
        print(f"找到{page_number}页数据.")
        for index in range(1, int(page_number) + 1):
            request = scrapy.Request(url=f'https://www.aznude.com/tags/vids/{self.cat}/1.html', callback=self.get_pages)
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
        name = f"{name1}{name2}{name3}.mp4"

        file = Path(r"D:\迅雷下载\aznude") / name
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
