from pathlib import Path

import requests
import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import urlparse, parse_qs

from tqdm import tqdm

import logging

logging.getLogger('scrapy').setLevel(logging.WARNING)
logging.getLogger('scrapy').propagate = False

logger = logging.getLogger('urllib3').setLevel(logging.WARNING)


def check_video_exists(url):
    response = requests.head(url)
    if response.status_code == 200:
        return True
    else:
        return False


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
    start_urls = ['https://tiktits.com/following?creator=130196']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

    def parse(self, response):
        followings = response.css("div.follower-item div.left-f div.ava-f a::attr('href')").getall()
        for following in followings:
            request = scrapy.Request(url=f"https://tiktits.com/{following}?sort=sortXLikeTv&dir=DESC&type=number&tv=1",
                                     callback=self.get_pages)
            yield request

    def get_pages(self, response):
        urls = response.css("div.item-grid div.link-over a::attr('href')").getall()
        parsed_url = urlparse(response.url)
        model = parsed_url.path.split('/')[2]
        # print(f"获取 {model} 的 {len(urls)} 个视频")
        for index, url in enumerate(urls):
            request = scrapy.Request(url=f"https://tiktits.com/{url}", callback=self.get_video)

            request.cb_kwargs["model"] = model
            yield request

    def get_video(self, response, model):
        url = response.css("meta[property='og:video']::attr('content')").get()
        url = url.replace('360.mp4', '1080.mp4')

        if not check_video_exists(url):
            url = url.replace('1080.mp4', '720.mp4')

        if not check_video_exists(url):
            url = url.replace('720.mp4', '360.mp4')

        parsed_response_url = urlparse(response.url)
        parsed_url = urlparse(url)

        new_name = f"[{model}][{parsed_url.path.split('/')[3].split('.')[0]}] {parsed_response_url.path.split('/')[2]}.mp4"
        old_name = f"{parsed_url.path.split('/')[3]}"

        old_file = Path(r"N:\PornWebCam\【tiktits】") / old_name
        new_file = Path(r"N:\PornWebCam\【tiktits】") / new_name

        if new_file.exists():
            return

        if old_file.exists():
            old_file.rename(new_file)
        else:
            print(url)


process = CrawlerProcess()
process.crawl(MySpider)
process.start()
