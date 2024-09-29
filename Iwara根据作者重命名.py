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
import logging


# logging.getLogger('scrapy').setLevel(logging.WARNING)
# logging.getLogger('scrapy').propagate = False


def validateTitle(title):
    return re.sub(r'[\\/:*?"<>|.]', '', title)


class MySpider(scrapy.Spider):
    name = 'my_spider'

    def start_requests(self):
        for video in Path(target).iterdir():
            if video.is_file():
                if video.name.startswith("Iwara"):
                    video_id = video.stem.replace('[Source]', '')
                    video_id = video_id.split('[')[-1].split(']')[0]
                    print(f"https://api.iwara.tv/video/{video_id}")
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50',
                        'Referer': f'https://www.iwara.tv/',
                        'Origin': f'https://www.iwara.tv',
                        'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjI1MmYyMjYyLWVjNjctNGU4Yi04OWI2LTdkOThjMDM4NmNhOSIsInR5cGUiOiJhY2Nlc3NfdG9rZW4iLCJyb2xlIjoidXNlciIsInByZW1pdW0iOmZhbHNlLCJpc3MiOiJpd2FyYSIsImlhdCI6MTcyNTc3NTMyOCwiZXhwIjoxNzI1Nzc4OTI4fQ.kpTvEebWlarNbJJ2L2Ibf2FiGA3xywe_rMybAVeesTI',
                    }
                    request = scrapy.Request(url=f"https://api.iwara.tv/video/{video_id}", headers=headers,
                                             callback=self.parse,
                                             meta={'handle_httpstatus_list': [403]})
                    request.cb_kwargs["file"] = video
                    yield request

    def parse(self, response, file):
        print(response)
        data_dict = json.loads(response.text)
        if response.status == 200:
            name1 = data_dict['user']['username']
            name2 = validateTitle(data_dict['user']['name'])
        elif response.status == 403:
            name1 = data_dict['data']['user']['username']
            name2 = validateTitle(data_dict['data']['user']['name'])
        else:
            print(response.status)
            return

        name = f"[{name1}] {name2}"
        print(name)
        if not (Path(target) / name).exists():
            (Path(target) / name).mkdir()
        file.rename(Path(target) / name / file.name)


settings = scrapy.settings.Settings()
settings.set('REQUEST_FINGERPRINTER_IMPLEMENTATION', '2.7')

process = CrawlerProcess(settings)
process.crawl(MySpider)
process.start()

# name_list = []
# for folder in Path(r"X:\MMD").iterdir():
#     name = folder.name.split(" ")[0]
#     if name in name_list:
#         print(name)
#     else:
#         name_list.append(name)