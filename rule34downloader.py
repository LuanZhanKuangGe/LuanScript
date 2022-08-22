import os
import sys
import scrapy
import json
from scrapy.crawler import CrawlerProcess

target = "garryswood"
data_dict = {}


class rule43spider(scrapy.Spider):
    name = target
    res = []
    fo = open("rule34.txt", "w")

    def start_requests(self):
        url = 'https://rule34.xxx/index.php?page=post&s=list&tags=3d+video+sound+' + target
        request = scrapy.Request(url=url, callback=self.get_page)
        yield request

    def get_page(self, response):
        print(response.url)
        urls = [response.url + "&pid=0"]
        pages = response.css("div#paginator").css("a")
        for page in pages:
            if not page.attrib.get("alt"):
                url = response.urljoin(page.attrib["href"])
                urls.append(url)
        for url in urls:
            request = scrapy.Request(url=url, callback=self.get_video)
            yield request

    def get_video(self, response):
        print(response.url)
        urls = response.css("span.thumb").css("a::attr(href)").getall()
        for url in urls:
            url = response.urljoin(url)
            request = scrapy.Request(url=url, callback=self.get_url)
            yield request

    def get_url(self, response):
        print(response.url)
        url = response.css("source::attr(src)").getall()[0]
        url = response.urljoin(url)
        self.res.append(url)

    def closed(self, response):
        for url in self.res:
            self.fo.write(url + '\n')
        print(len(self.res))


if __name__ == "__main__":
    process = CrawlerProcess({"LOG_LEVEL": "WARNING"})
    process.crawl(rule43spider)
    process.start()


