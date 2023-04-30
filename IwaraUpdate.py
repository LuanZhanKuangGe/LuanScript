import logging
import os
import re
import shutil

import scrapy
import urllib
from scrapy.crawler import CrawlerProcess
import tkinter as tk
from tkinter import filedialog
from pathlib import Path

root = tk.Tk()
root.withdraw()
target = filedialog.askdirectory() + r"//"

def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"
    new_title = re.sub(rstr, "_", title)
    return new_title

class iwara(scrapy.Spider):
    name = 'iwara'

    def start_requests(self):
        for folder in Path(target).iterdir():
            if folder.is_dir() and not folder.name.startswith("["):
                request = scrapy.Request(url=f"https://ecchi.iwara.tv/users/{folder.name}", callback=self.parse)
                request.cb_kwargs["old_name"] = folder
                yield request

    def parse(self, response, old_name):
        if response.status != 200:
            print(response.request.url)
            print(f"{old_name.name} failed {response.status}")


if __name__ == "__main__":
    # level = "INFO"
    # process = CrawlerProcess({"LOG_LEVEL": level})
    # process.crawl(iwara)
    # process.start()

    for folder in Path(target).iterdir():
        if folder.is_dir() and not folder.name.startswith("["):
            size = len(list(folder.iterdir()))
            if size == 0:
                os.rmdir(folder)