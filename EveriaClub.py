import shutil
from pathlib import Path

import requests
import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import urlparse, parse_qs
import zipfile

from tqdm import tqdm

import re
import logging

logging.getLogger('scrapy').setLevel(logging.ERROR)
logging.getLogger('scrapy').propagate = False

def validateTitle(title):
    return re.sub(r'[\\/:*?"<>|]', '', title)

class MySpider(scrapy.Spider):
    name = 'madoucun_cosplay'
    # start_urls = ['https://everia.club/category/cosplay/']
    # target_path = Path(r'N:\HentaiPicture\EveriaClub\Cosplay')
    start_urls = ['https://everia.club/category/korea/']
    target_path = Path(r'N:\HentaiPicture\EveriaClub\Korea')
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

    def parse(self, response):
        page_number = response.css('ul.page-numbers li a.page-numbers::text').getall()[-2]
        page_number = 2
        for index in range(1, int(page_number) + 1):
            request = scrapy.Request(url=f'{self.start_urls[0]}page/{index}/', callback=self.get_pages)
            yield request

    def get_pages(self, response):
        image_packs = response.css('div.content div.img-wrap a::attr(href)').getall()
        for image_pack in image_packs:
            request = scrapy.Request(url=f"{image_pack}", callback=self.get_pack)
            yield request

    def get_pack(self, response):
        title = response.css('h1.title::text').get()
        title = validateTitle(title)
        images = response.css('figure.wp-block-image img::attr(data-src)').getall()

        if len(images) == 0:
            images = response.css('div.separator a img::attr(data-src)').getall()

        folder = self.target_path / f"{title}"
        zip_file = self.target_path / f"{title}.zip"
        if zip_file.exists():
            print(f"{zip_file} 已存在")
            return

        Path(folder).mkdir(exist_ok=True)

        progress_bar = tqdm(desc=folder.name, total=len(images))

        for image in images:
            request = scrapy.Request(url=image, callback=self.save_image)
            request.cb_kwargs["folder"] = folder
            request.cb_kwargs["process"] = len(images)
            request.cb_kwargs["progress_bar"] = progress_bar
            yield request

    def save_image(self, response, folder, process, progress_bar):

        if response.status == 404:
            print(f"{folder} got 404")
            shutil.rmtree(folder)
            return

        filename = response.url.split("/")[-1]
        filename = validateTitle(filename)
        with open(Path(folder)/filename, 'wb') as f:
            f.write(response.body)
            progress_bar.update(1)

        if len(list(Path(folder).iterdir())) == process:
            with zipfile.ZipFile(self.target_path / f"{folder.name}.zip", 'w') as zipf:
                for file in folder.iterdir():
                    zipf.write(file, file.name)
            shutil.rmtree(folder)


process = CrawlerProcess()
process.crawl(MySpider)
process.start()
