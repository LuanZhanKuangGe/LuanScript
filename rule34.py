from pathlib import Path

import scrapy
from scrapy.crawler import CrawlerProcess
from luanfunc import download_video

import logging
# logging.getLogger('scrapy').setLevel(logging.WARNING)
# logging.getLogger('scrapy').propagate = False


class MySpider(scrapy.Spider):
    name = 'main'
    allowed_domains = ['rule34.xxx']
    file_exist = []
    start_urls = ["https://rule34.xxx/"]

    artist = "all"

    def start_requests(self):
        for file in sorted(Path(r'X:\rule34').glob('**/*.mp4')):
            self.file_exist.append(file.stem.split("_")[-1])

        counter = 0
        if not hasattr(self, 'artist') or self.artist == "all":
            for artist in Path(r'X:\rule34').iterdir():
                if artist.is_dir():
                    counter += 1
                    url = 'https://rule34.xxx/index.php?page=post&s=list&tags=video+sound+' + artist.name
                    request = scrapy.Request(url=url, callback=self.get_page)
                    request.cb_kwargs["artist"] = artist.name
                    request.cb_kwargs["check_all"] = True
                    request.cb_kwargs["counter"] = counter
                    yield request
        else:
            artist_name = self.artist
            url = 'https://rule34.xxx/index.php?page=post&s=list&tags=video+sound+' + artist_name
            request = scrapy.Request(url=url, callback=self.get_page)
            request.cb_kwargs["artist"] = artist_name
            request.cb_kwargs["check_all"] = False
            request.cb_kwargs["counter"] = counter
            yield request

    def get_page(self, response, artist, check_all, counter):
        urls = [response.url + "&pid=0"]
        pages = response.css("div#paginator").css("a")
        for page in pages:
            if not page.attrib.get("alt"):
                url = response.urljoin(page.attrib["href"])
                urls.append(url)
        if check_all:
            request = scrapy.Request(url=urls[0], callback=self.get_video)
            request.cb_kwargs["artist"] = artist
            request.cb_kwargs["counter"] = counter
            yield request
        else:
            for url in urls:
                request = scrapy.Request(url=url, callback=self.get_video)
                request.cb_kwargs["artist"] = artist
                request.cb_kwargs["counter"] = counter
                yield request

    def get_video(self, response, artist, counter):
        urls = response.css("span.thumb").css("a::attr(href)").getall()
        for url in urls:
            if url.split("=")[-1] not in self.file_exist:
                url = response.urljoin(url)
                request = scrapy.Request(url=url, callback=self.get_url)
                request.cb_kwargs["artist"] = artist
                request.cb_kwargs["counter"] = counter
                yield request

    def get_url(self, response, artist, counter):
        if response.css("source::attr(src)").getall():
            url = response.css("source::attr(src)").getall()[0]
            url = response.urljoin(url)
            name = f"{artist}_{url.split('?')[-1]}.mp4"
            path = Path(r'X:\rule34') / artist
            file = path / name
            url = url.split('?')[0]

            if not path.exists():
                path.mkdir()

            if not file.exists():
                if download_video(url, url, file):
                    print(f"{counter} {artist} {file} 下载成功")
                else:
                    print(f"{counter} {artist} {file} 下载失败")
                    file.unlink()
            else:
                print(f"{file} 已存在")


settings = scrapy.settings.Settings()
settings.set('REQUEST_FINGERPRINTER_IMPLEMENTATION', '2.7')
settings.set('DOWNLOAD_DELAY', '1')

process = CrawlerProcess(settings)
process.crawl(MySpider)
process.start()