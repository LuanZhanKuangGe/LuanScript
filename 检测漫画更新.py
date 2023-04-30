import os

import scrapy
import html

urls = []
# 定义目标文件夹路径
folder_path = r'N:\HentaiPicture\Manga'

# 遍历目标文件夹
for root, dirs, files in os.walk(folder_path):
    for filename in files:
        # 判断文件名是否包含指定字符串
        if '[中国翻訳]' not in filename and '[DL版]' not in filename:
            # 打印符合条件的文件名
            urls.append(f"https://btsow.boats/search/{filename}")

def is_contain_string(A):
    strings = ['中国', 'DL版', 'Chinese', '汉化', '翻译', '翻訳']
    entities = [html.escape(s) for s in strings]
    for s in entities:
        if s in A:
            return True
    return False

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = urls
    download_delay = 5
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

    def parse(self, response):
        datas = response.xpath('//div[@class="data-list"]/div[@class="row"]/a')
        for data in datas:
            if is_contain_string(data.xpath('.//@title').get()):
                print(data.xpath('.//@title').get(), f"https:{data.xpath('.//@href').get()}")


# 运行爬虫程序
from scrapy.crawler import CrawlerProcess

process = CrawlerProcess()
process.crawl(MySpider)
process.start()