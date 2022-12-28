from pathlib import Path

import scrapy
from ..items import urlItem


class MainSpider(scrapy.Spider):
    name = 'main'
    allowed_domains = ['rule34.xxx']
    file_exist = []
    start_urls = ["https://rule34.xxx/"]

    def start_requests(self):
        for file in sorted(Path('N:\\HentaiVideo\\rule34\\').glob('**/*.mp4')):
            self.file_exist.append(file.stem.split("_")[-1])

        if not hasattr(self, 'artist') or self.artist == "all":
            for artist in Path('N:\\HentaiVideo\\rule34\\').iterdir():
                if artist.is_dir():
                    url = 'https://rule34.xxx/index.php?page=post&s=list&tags=3d+video+sound+' + artist.name
                    request = scrapy.Request(url=url, callback=self.get_page)
                    request.cb_kwargs["artist"] = artist.name
                    request.cb_kwargs["all"] = True
                    yield request
        else:
            artist_name = self.artist
            url = 'https://rule34.xxx/index.php?page=post&s=list&tags=3d+video+sound+' + artist_name
            request = scrapy.Request(url=url, callback=self.get_page)
            request.cb_kwargs["artist"] = artist_name
            request.cb_kwargs["all"] = False
            yield request



    def get_page(self, response, artist, all):
        urls = [response.url + "&pid=0"]
        pages = response.css("div#paginator").css("a")
        for page in pages:
            if not page.attrib.get("alt"):
                url = response.urljoin(page.attrib["href"])
                urls.append(url)
        if all:
            request = scrapy.Request(url=urls[0], callback=self.get_video)
            request.cb_kwargs["artist"] = artist
            yield request
        else:
            for url in urls:
                request = scrapy.Request(url=url, callback=self.get_video)
                request.cb_kwargs["artist"] = artist
                yield request

    def get_video(self, response, artist):
        urls = response.css("span.thumb").css("a::attr(href)").getall()
        for url in urls:
            if url.split("=")[-1] not in self.file_exist:
                url = response.urljoin(url)
                request = scrapy.Request(url=url, callback=self.get_url)
                request.cb_kwargs["artist"] = artist
                yield request
            else:
                print(url, "already exist.")

    def get_url(self, response, artist):
        url_item = urlItem()

        if response.css("source::attr(src)").getall():
            url = response.css("source::attr(src)").getall()[0]
            url = response.urljoin(url)
            url_item['file_urls'] = url.split('?')[0]

            name = artist + '_'

            url_item['original_file_name'] = name + url.split('?')[1] + ".mp4"
            url_item['file_urls'] = url_item['file_urls'] + '?' + name + url.split('?')[1]

            yield url_item
