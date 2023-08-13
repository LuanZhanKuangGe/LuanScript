from pathlib import Path

import requests
import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import urlparse, parse_qs

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tqdm import tqdm

import logging

logging.getLogger('scrapy').setLevel(logging.WARNING)
logging.getLogger('scrapy').propagate = False


def download_video(url, ref, filename):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Referer': ref,
        'Origin': ref
    }

    response = requests.get(url, stream=True, headers=headers)

    total_size = int(response.headers.get('Content-Length', 0))

    block_size = 1024
    progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)

    with open(filename, 'wb') as f:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            f.write(data)

    progress_bar.close()
    if total_size != 0 and progress_bar.n != total_size:
        return 0
    return 1


class MySpider(scrapy.Spider):
    name = 'videocelebs_spider'
    start_urls = ['https://videocelebs.net/most-popular']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

    def __init__(self, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.driver = webdriver.Chrome()

    def parse(self, response):
        page_number = response.css('div.wp-pagenavi a.last::text').get()
        page_number = 1
        print(f"找到{page_number}页数据.")
        for index in range(1, int(page_number) + 1):
            request = scrapy.Request(url=f"https://videocelebs.net/most-popular/page/{index}", callback=self.get_pages)
            request.cb_kwargs["index"] = index
            yield request

    def get_pages(self, response, index):
        urls = response.css("div.list_videos div.item a::attr('href')").getall()
        print(f"第{index}页，找到{len(urls)}个视频")
        video_index = 0
        url = urls[0]
        # for video_index, url in enumerate(urls):
        request = scrapy.Request(url=url, callback=self.get_video)
        request.cb_kwargs["index"] = index
        request.cb_kwargs["video_index"] = video_index
        yield request

    def get_video(self, response, index, video_index):
        title = response.css('h1::text').get()
        # print(response.css('div.player-wrap').get())
        print(title)

        js_string = response.css('div.player-holder script').getall()[1]
        jss = js_string.split('function/0/')
        for js in jss:
            if '.mp4' in js:
                url = js.split('.mp4')[0] + '.mp4/'
        # rnd: \'1691890323\',
        # rnd = js_string.split("rnd: \'")[1].split("\',")[0]
        # url  = f"{url}/?rnd={rnd}"
        print(url)

        self.driver.get(response.url)

        element = self.driver.find_element(By.CLASS_NAME, 'player-wrap')
        print(element.get_attribute('outerHTML'))

        element.click()

        element = self.driver.find_element(By.ID, 'kt_player')
        print(element.get_attribute('outerHTML'))

        element.click()

        element = self.driver.find_element(By.CLASS_NAME, 'fp-player')
        print(element.get_attribute('outerHTML'))

        element.click()

        self.driver.implicitly_wait(10)

        element = self.driver.find_element(By.CLASS_NAME, 'fp-player')
        print(element.get_attribute('outerHTML'))


        # # self.driver.implicitly_wait(10)
        # # 使用Selenium模拟点击操作
        # element = WebDriverWait(self.driver, 10).until(
        #     EC.presence_of_element_located((By.XPATH, '//div[@class="player-wrap"]'))
        # )
        #
        # element.click()
        #
        #
        # # 等待一段时间，确保点击操作生效并加载内容
        # self.driver.implicitly_wait(10)
        #
        #
        # # 获取点击后的页面内容
        # clicked_response = scrapy.http.HtmlResponse(
        #     url=self.driver.current_url,
        #     body=self.driver.page_source,
        #     encoding='utf-8',
        # )
        #
        # print(response.css('div.kt-player').get())
        # print(response.css('div.kt-player div.fp-player').get())
        #
        # print(clicked_response.css('div.kt-player').get())
        # print(clicked_response.css('div.kt-player div.fp-player').get())
        #
        # self.driver.get(clicked_response.url)
        #
        # element2 = WebDriverWait(self.driver, 10).until(
        #     EC.element_to_be_clickable((By.XPATH, '//div[@id="kt-player"]'))
        # )
        # element2.click()
        #
        # self.driver.implicitly_wait(10)
        #
        # clicked_response = scrapy.http.HtmlResponse(
        #     url=self.driver.current_url,
        #     body=self.driver.page_source,
        #     encoding='utf-8',
        # )
        #
        # print(clicked_response.css('div.kt-player div.fp-player').get())
        # print(clicked_response.css('div.kt-player fp-message').get())
        #
        #
        #
        # # 等待一段时间，确保点击操作生效并加载内容
        # self.driver.implicitly_wait(10)

        # parsed_url = urlparse(response.url)
        # id = parsed_url.path.split('/')[1]
        # title = parsed_url.path.split('/')[2]
        # name = f"[{id}]{title}.mp4"
        #
        # parsed_url = urlparse(response.css("iframe::attr(src)").get())
        # params = parse_qs(parsed_url.query)
        # video = f"{params['fileid'][0]}.mp4"

        # file = Path(r"N:\PornWebCam\【fyptt】") / name
        # if not file.exists():
        #     if download_video(f"https://stream.fyptt.to/{video}", response.url, file):
        #         print(f"第{index}页 第{video_index + 1}个视频 {name} 下载成功")
        #     else:
        #         print(f"第{index}页 第{video_index + 1}个视频 {name} 下载失败")
        #         file.unlink()
        # else:
        #     print(f"第{index}页 第{video_index + 1}个视频 {name} 已存在")

    # def closed(self, reason):
    #     self.driver.quit()

settings = scrapy.settings.Settings()
settings.set('REQUEST_FINGERPRINTER_IMPLEMENTATION', '2.7')

process = CrawlerProcess(settings)
process.crawl(MySpider)
process.start()
