import datetime
from pathlib import Path
import scrapy
import json
from scrapy.crawler import CrawlerProcess
import re

target = r"X:\MMD"

with open('data.json', 'r', encoding='utf-8') as file:
    database = json.load(file)

output = {}


# logging.getLogger('scrapy').setLevel(logging.WARNING)
# logging.getLogger('scrapy').propagate = False


def validateTitle(title):
    return re.sub(r'[\\/:*?"<>|.]', '', title)


class MySpider(scrapy.Spider):
    name = 'my_spider'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50',
        'Referer': f'https://www.iwara.tv/',
        'Origin': f'https://www.iwara.tv',
        'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjI1MmYyMjYyLWVjNjctNGU4Yi04OWI2LTdkOThjMDM4NmNhOSIsInR5cGUiOiJhY2Nlc3NfdG9rZW4iLCJyb2xlIjoidXNlciIsInByZW1pdW0iOmZhbHNlLCJpc3MiOiJpd2FyYSIsImlhdCI6MTcxODI5MDIyOCwiZXhwIjoxNzE4MjkzODI4fQ.7Pqau0fu-7tSu8YPMMbYNTVbffmyfUXpx92Y_2FyjCA',
    }

    def start_requests(self):
        for folder in Path(target).iterdir():
            if folder.is_dir() and folder.name.startswith('['):
                name = folder.stem.split(']')[0][1:]
                # if name not in ['113458', 'ratzy']:
                #     continue
                output[name] = {}
                output[name]['name'] = folder.stem.split(' ')[1]
                output[name]['all'] = 0
                output[name]['fav'] = 0
                output[name]['new_have'] = 0
                output[name]['all_have'] = len(list(folder.iterdir()))
                modification_time = folder.stat().st_mtime
                modification_date = datetime.datetime.fromtimestamp(modification_time).date()
                output[name]['update_time'] = str(modification_date)
                output[name]['url'] = f"https://www.iwara.tv/profile/{name}/videos"
                url = f"https://api.iwara.tv/profile/{name}"
                print(url)
                request = scrapy.Request(url=url, headers=self.headers, callback=self.parse,
                                         meta={'handle_httpstatus_list': [403]})
                yield request

    def parse(self, response):
        print(response)
        data_dict = json.loads(response.text)
        if response.status == 200:
            user_id = data_dict['user']['id']
            for i in range(10):
                url = f"https://api.iwara.tv/videos?sort=likes&page={i}&user={user_id}"
                print(url)
                request = scrapy.Request(url=url, headers=self.headers, callback=self.parse2,
                                         meta={'handle_httpstatus_list': [403]})
                yield request
        elif response.status == 403:
            print(response.status)

    def parse2(self, response):
        print(response)
        data_dict = json.loads(response.text)
        if response.status == 200:
            for result in data_dict['results']:
                if not result.get('file'):
                    print(f"skip https://www.iwara.tv/video/{result['id']}")
                    continue

                if result['file']['path'].split('/')[0] in ['2023', '2024']:
                    user = result['user']['username']
                    output[user]['all'] += 1
                    if result['id'].lower() in database['mmd_data']:
                        output[user]['new_have'] += 1
                    if int(result['numLikes']) > 500:
                        output[user]['fav'] += 1

        elif response.status == 403:
            print(response.status)


settings = scrapy.settings.Settings()
settings.set('REQUEST_FINGERPRINTER_IMPLEMENTATION', '2.7')

process = CrawlerProcess(settings)
process.crawl(MySpider)
process.start()

with open("tmp.json", "w", encoding="utf8") as fp:
    json.dump(output, fp, ensure_ascii=False)

print(output)
