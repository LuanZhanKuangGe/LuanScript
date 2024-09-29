from pathlib import Path
import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import urlparse, parse_qs
from func import download_video, validateTitle, scrapy_settings
import logging
import re

# 设置Scrapy的日志级别为WARNING,并禁止传播
logging.getLogger('scrapy').setLevel(logging.WARNING)
logging.getLogger('scrapy').propagate = False

def validateTitle(title):
    if not isinstance(title, str):
        return ""  # 或者可以选择返回 str(title)
    return re.sub(r'[\\/:*?"<>|.]', '_', title)

class oreno3dSpider(scrapy.Spider):
    name = 'oreno_spider'
    start_urls = ['https://oreno3d.com']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

    def parse(self, response):
        directory = r"X:\MMD\#Del\test"
        path = Path(directory)
        for file in path.rglob('*'):
            if file.is_file():
                new_name = file.stem.split('[Deleted]')[1]
                url = f"https://oreno3d.com/search?keyword={new_name}"
                yield scrapy.Request(url, callback=self.parse_search_results, cb_kwargs={"file": file, "new_name": new_name})

    def parse_search_results(self, response, file, new_name):
        # 处理搜索结果页面
        res = response.css('article').getall()
        if len(res) == 0:
            print(f"未找到{new_name}相关视频")
        elif len(res) == 1:
            find_name = response.css('article a h2::text').get()
            find_name = validateTitle(find_name)
            if not find_name:
                print(f"{new_name}转换失败")
            if find_name == new_name:
                url = response.css('article a::attr(href)').get()
                yield scrapy.Request(url, callback=self.parse_video_page, cb_kwargs={"file": file, "new_name": new_name})       

            else:
                print(f"{new_name}名字无法对应")
        else:
            print(f"找到多个{new_name}相关视频")

    def parse_video_page(self, response, file, new_name):
        url = response.css('article a::attr(href)').get()
        id = urlparse(url).path.split('/')[-1]
        print(f"找到{new_name}相关视频, id为{id}")
        new_name = f"Iwara - {new_name} [{id}] [Source].mp4"
        # 重命名文件
        new_file_path = file.with_name(new_name)
        print(f"{file.name}重命名为{new_file_path.name}")
        file.rename(new_file_path)
            
if __name__ == "__main__":
    # 创建并启动爬虫进程
    process = CrawlerProcess(settings=scrapy_settings)
    process.crawl(oreno3dSpider)
    process.start()