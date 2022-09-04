from pathlib import Path

import scrapy
from ..items import urlItem

arist = "bulgingsenpai"


class MainSpider(scrapy.Spider):
    name = 'main'
    allowed_domains = ['rule34.xxx']
    target = arist
    file_exist = []
    start_urls = ["https://rule34.xxx/"]

    def start_requests(self):
        for file in sorted(Path('V:\\rule34\\').glob('**/*.mp4')):
            self.file_exist.append(file.stem.split("_")[-1])
        url = 'https://rule34.xxx/index.php?page=post&s=list&tags=3d+video+sound+' + self.target
        request = scrapy.Request(url=url, callback=self.get_page)
        yield request

    def get_page(self, response):
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
        urls = response.css("span.thumb").css("a::attr(href)").getall()
        for url in urls:
            if url.split("=")[-1] not in self.file_exist:
                url = response.urljoin(url)
                request = scrapy.Request(url=url, callback=self.get_url)
                yield request
            else:
                print(url, "already exist.")

    def get_url(self, response):
        url_item = urlItem()

        if response.css("source::attr(src)").getall():
            url = response.css("source::attr(src)").getall()[0]
            url = response.urljoin(url)
            url_item['file_urls'] = url.split('?')[0]

            name = ''
            artists = response.css('li.tag-type-artist').css('a::text').getall()
            if len(artists) == 0:
                artists.append('no-name')
            for artist in artists:
                artist = artist.replace('(artist)', '')
                artist = artist.strip()
                artist = artist.replace(' ', '-')
                name += artist + '_'

            url_item['original_file_name'] = name + url.split('?')[1] + ".mp4"
            url_item['file_urls'] = url_item['file_urls'] + '?' + name + url.split('?')[1]

            yield url_item
