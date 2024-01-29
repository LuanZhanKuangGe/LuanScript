import json
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
    custom_string = f"{filename.name}"
    progress_bar.set_description(custom_string)

    with open(filename, 'wb') as f:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            f.write(data)

    progress_bar.close()
    if total_size != 0 and progress_bar.n != total_size:
        return 0
    return 1


class MySpider(scrapy.Spider):
    name = 'xfree_spider'
    start_urls = ['https://www.xfree.com']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'Referer': f'https://www.xfree.com/',
        'Origin': f'https://www.xfree.com',
        'apiversion': '1.0'
         }
    tag_name = [("Dancing", 4591), ("PoleDance", 118820), ("TiktokPorn", 160996), ("TiktokLeaks", 181453)]
    delete_list =[285085,316143,316143,316154,316253,285634,285634,285639,284869]
    tag_id = 181453
    offset = 0
    counter = 0

    def parse(self, response):
        request = scrapy.Request(url=f"https://www.xfree.com/api/post/?limit=30&offset={self.offset}&tagId={self.tag_id}&lgbt=1", headers=self.headers, callback=self.get_pages)
        yield request


    def get_pages(self, response):
        data = json.loads(response.body)
        items = data['body']
        for item in items:
            file = Path(r"N:\PornWebCam\【xfree】")/f"{item['id']}.mp4"
            if file.exists():
                print(f"{item['id']}已存在")
            elif int(item['id']) not in self.delete_list:
                request = scrapy.Request( url=f"https://www.xfree.com/video?id={item['id']}",headers=self.headers, callback=self.get_video)
                yield request
        self.counter += len(items)
        if self.counter % 30 == 0:
            self.offset += 30
            request = scrapy.Request(
                url=f"https://www.xfree.com/api/post/?limit=30&offset={self.offset}&tagId={self.tag_id}&lgbt=1", headers=self.headers, callback=self.get_pages)
            yield request
        else:
            print(f"共{self.counter}个视频")

    def get_video(self, response):
        video_id = response.url.split('?id=')[1]
        file = Path(r"N:\PornWebCam\【xfree】") / f"{video_id}.mp4"
        video_url = response.css('meta[property="og:video"]::attr(content)').get()
        video_url = video_url.replace("full.mp4", "full-d.mp4")
        print(video_id, video_url)

        if download_video(video_url, response.url, file):
            print(f"视频 {video_id} {video_url} 下载成功")
        else:
            print(f"视频 {video_id} {video_url} 下载失败")
            file.unlink()


settings = scrapy.settings.Settings()
settings.set('REQUEST_FINGERPRINTER_IMPLEMENTATION', '2.7')

process = CrawlerProcess(settings)
process.crawl(MySpider)
process.start()
