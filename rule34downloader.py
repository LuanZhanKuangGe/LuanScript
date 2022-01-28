import os
import re
import scrapy
import urllib.request
from scrapy.crawler import CrawlerProcess
import progressbar
from tqdm import tqdm

pbar = None


def show_progress(block_num, block_size, total_size):
    global pbar
    if pbar is None:
        pbar = progressbar.ProgressBar(maxval=total_size)
        pbar.start()

    downloaded = block_num * block_size
    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()
        pbar = None


class iwaraSpider(scrapy.Spider):
    name = "rule34xxx"
    url = "https://rule34.xxx/index.php?page=favorites&s=view&id=1178285"

    def start_requests(self):
        request = scrapy.Request(url=self.url, callback=self.parse)
        yield request

    def parse(self, response):
        last = response.css("div#paginator").css("a::attr(onclick)").getall()[-1]
        last = last.split("pid=")[1]
        last = last.split("'; ")[0]
        page = int(int(last) / 50) + 1
        print("收藏总页数 : ", page)

        for i in range(page):
            url = self.url + "&pid=" + str(i * 50)
            request = scrapy.Request(url=url, callback=self.parse2)
            yield request

    def parse2(self, response):
        urls = response.css("span.thumb").css("a::attr(href)").getall()
        for url in urls:
            file = os.path.join("Z:", "rule34", url.split("id=")[1] + ".mp4")
            url = "https://rule34.xxx/" + url
            if not os.path.exists(file):
                request = scrapy.Request(url=url, callback=self.parse3)
                yield request

    def parse3(self, response):
        url = response.css("source::attr(src)").getall()
        src = url[0].split("?")[0]
        name = url[0].split("?")[1] + ".mp4"
        print(name + " download start!!!!!")
        urllib.request.urlretrieve(src, name, show_progress)
        print(name + " download stop!!!!!")


if __name__ == "__main__":
    process = CrawlerProcess({"LOG_LEVEL": "INFO"})
    process.crawl(iwaraSpider)
    process.start()
