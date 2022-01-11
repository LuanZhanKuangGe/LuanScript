import os
import re
import scrapy
from scrapy.crawler import CrawlerProcess

def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"
    new_title = re.sub(rstr, "_", title)
    return new_title

class r34AnimSpider(scrapy.Spider):
    name = "r34anim"
    fo = open("r34anim.txt", "w")

    def start_requests(self):
        for i in range(5):
            url = "https://www.r34anim.com/rule34-tag/sound/page/"+ str(i+1) +"/"
            request = scrapy.Request(url=url, callback=self.parse)
            yield request

    def parse(self, response):
        urls = response.css('div.post-thumbnail').css('a[title]::attr(href)').getall()
        for url in urls:
            request = scrapy.Request(url=url, callback=self.parse2)
            yield request

    def parse2(self, response):
        url = response.css('video.wp-video-shortcode').css('a::attr(href)').get()
        print("--------" + url)
        self.fo.write( url +"\n")

if __name__ == "__main__":
    level = "INFO"
    process = CrawlerProcess({"LOG_LEVEL": level})
    process.crawl(r34AnimSpider)
    process.start()