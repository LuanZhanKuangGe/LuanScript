from pathlib import Path

import requests
import scrapy
import json
from scrapy.crawler import CrawlerProcess
from urllib.parse import urlparse, parse_qs

from tqdm import tqdm
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()
target = filedialog.askdirectory() + r"//"
import re

with open('data.json', 'r', encoding='utf-8') as file:
    database = json.load(file)

output = {}

# logging.getLogger('scrapy').setLevel(logging.WARNING)
# logging.getLogger('scrapy').propagate = False


def validateTitle(title):
    return re.sub(r'[\\/:*?"<>|.]', '', title)


class MySpider(scrapy.Spider):
    name = 'my_spider'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50',
        'Referer': f'https://www.iwara.tv/',
        'Origin': f'https://www.iwara.tv',
        'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjI1MmYyMjYyLWVjNjctNGU4Yi04OWI2LTdkOThjMDM4NmNhOSIsInR5cGUiOiJhY2Nlc3NfdG9rZW4iLCJyb2xlIjoidXNlciIsInByZW1pdW0iOmZhbHNlLCJpc3MiOiJpd2FyYSIsImlhdCI6MTcxODI5MDIyOCwiZXhwIjoxNzE4MjkzODI4fQ.7Pqau0fu-7tSu8YPMMbYNTVbffmyfUXpx92Y_2FyjCA',
    }

    def start_requests(self):
        for folder in Path(target).iterdir():
            if folder.is_dir() and folder.name.startswith('['):
                name = folder.stem.split(']')[0][1:]
                output[name] = 0
                url = f"https://api.iwara.tv/profile/{name}"
                print(url)
                request = scrapy.Request(url=url, headers=self.headers, callback=self.parse,
                                         meta={'handle_httpstatus_list': [403]})
                yield request


    def parse(self, response):
        print(response)
        data_dict = json.loads(response.text)
        if response.status == 200:
            user_id = data_dict['user']['id']
            for i in range(10):
                url = f"https://api.iwara.tv/videos?sort=likes&page={i}&user={user_id}"
                print(url)
                request = scrapy.Request(url=url, headers=self.headers, callback=self.parse2,
                                        meta={'handle_httpstatus_list': [403]})
                yield request
        elif response.status == 403:
            print(response.status)

    def parse2(self, response):
        print(response)
        data_dict = json.loads(response.text)
        if response.status == 200:
            for result in data_dict['results']:
                if result['id'] not in database['mmd_data'] and int(result['numLikes'])>500 and result['file']['path'].split('/')[0] in ['2023', '2024']:
                    print(result['id'], result['title'], result['numLikes'])
                    user = result['user']['username']
                    output[user] += 1
        elif response.status == 403:
            print(response.status)


settings = scrapy.settings.Settings()
settings.set('REQUEST_FINGERPRINTER_IMPLEMENTATION', '2.7')

process = CrawlerProcess(settings)
process.crawl(MySpider)
process.start()

sorted_keys = sorted(output, key=output.get, reverse=True)
sorted_dict = {k: output[k] for k in sorted_keys}
with open("tmp.json", "w", encoding="utf8") as fp:
    json.dump(sorted_dict, fp, ensure_ascii=False)

print(sorted_dict)