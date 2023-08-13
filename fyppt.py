from pathlib import Path

import requests
import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import urlparse, parse_qs

from tqdm import tqdm

import logging

logging.getLogger('scrapy').setLevel(logging.WARNING)
logging.getLogger('scrapy').propagate = False


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
    name = 'fyptt_spider'
    start_urls = ['https://fyptt.to']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

    def parse(self, response):
        page_number = response.css('ul.page-numbers li:nth-last-child(2) a::text').get()
        page_number = 1
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

    def get_video(self, response, index, video_index):
        parsed_url = urlparse(response.url)
        id = parsed_url.path.split('/')[1]
        title = parsed_url.path.split('/')[2]
        name = f"[{id}]{title}.mp4"

        parsed_url = urlparse(response.css("iframe::attr(src)").get())
        params = parse_qs(parsed_url.query)
        video = f"{params['fileid'][0]}.mp4"

        file = Path(r"N:\PornWebCam\【fyptt】") / name
        if not file.exists():
            if download_video(f"https://stream.fyptt.to/{video}", response.url, file):
                print(f"第{index}页 第{video_index + 1}个视频 {name} 下载成功")
            else:
                print(f"第{index}页 第{video_index + 1}个视频 {name} 下载失败")
                file.unlink()
        else:
            print(f"第{index}页 第{video_index + 1}个视频 {name} 已存在")


settings = scrapy.settings.Settings()
settings.set('REQUEST_FINGERPRINTER_IMPLEMENTATION', '2.7')

process = CrawlerProcess(settings)
process.crawl(MySpider)
process.start()
