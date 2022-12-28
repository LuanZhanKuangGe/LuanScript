from pathlib import Path

import scrapy
from scrapy.crawler import CrawlerProcess


class check_HD(scrapy.Spider):
    name = "checker"

    def start_requests(self):
        for actor in Path(r"N:\AV").iterdir():
            if actor.is_dir():
                for video in actor.rglob("*.nfo"):
                    # print(video.parents[0].parts[-1])
                    if video.parents[0].parts[-1] == 'Watermark':
                        url = "https://www.141jav.com/search/" + video.stem.split(" ")[0].replace("-", "")
                        request = scrapy.Request(url=url, callback=self.parse)
                        yield request

    def parse(self, response):
        res = response.css("div.card-content").getall()
        if len(res) == 0:
            print(response.request.url, "no HD torrent found ...")
        else:
            print(response.request.url, "HD torrent found !!!")


if __name__ == "__main__":
    level = "INFO"
    process = CrawlerProcess({"LOG_LEVEL": level})
    process.crawl(check_HD)
    process.start()
