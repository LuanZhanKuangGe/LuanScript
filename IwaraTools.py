import logging
import os
import re
import shutil

import scrapy
from scrapy.crawler import CrawlerProcess
import tkinter as tk
from tkinter import filedialog
from pathlib import Path


root = tk.Tk()
root.withdraw()
target = filedialog.askdirectory()+r"//"


def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"
    new_title = re.sub(rstr, "_", title)
    return new_title


class iwaraSpider(scrapy.Spider):
    name = "renamer"

    def start_requests(self):
        for files in os.listdir(target):
            if files.lower().endswith("source.mp4"):
                url = "https://www.iwara.tv/videos/" + files.split("_")[1]
                request = scrapy.Request(url=url, callback=self.parse)
                request.cb_kwargs["oldname"] = target + files
                yield request
            elif files.lower().find("source.mp4.") != -1:
                print("发现未完成下载 https://www.iwara.tv/videos/" + files.split("_")[1])

    def parse(self, response, oldname):
        newname = (
            response.css("a.username::text").get()
            + " - "
            + response.css("h1.title::text").get()
        )
        newname = validateTitle(newname)
        newname = target + newname + ".mp4"
        if os.path.exists(newname):
            print(newname + "已存在,请自行修改" + oldname)
            return
        print(oldname + " 重命名为 " + newname)
        os.rename(oldname, newname)


if __name__ == "__main__":
    # level = "INFO"
    # process = CrawlerProcess({"LOG_LEVEL": level})
    # process.crawl(iwaraSpider)
    # process.start()
    for file in os.listdir(target):
        old_file = Path(target)/Path(file)
        if old_file.suffix == '.mp4' and file.find(" - ") != -1:
            arist = file.split(" - ")[0]
            if arist.find(".") == -1:
                Path.mkdir(Path(target)/arist, exist_ok=True)
                new_file = Path(target)/old_file.parent/arist/old_file.name
                print(str(old_file) + " 移动到 " + str(new_file))
                shutil.move(old_file, new_file)

