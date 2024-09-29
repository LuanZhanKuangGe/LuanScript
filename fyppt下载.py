from pathlib import Path
import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import urlparse, parse_qs
from func import download_video, validateTitle, scrapy_settings
import logging

# 设置Scrapy的日志级别为WARNING,并禁止传播
logging.getLogger('scrapy').setLevel(logging.WARNING)
logging.getLogger('scrapy').propagate = False

# 添加以下代码来禁用urllib3的日志
logging.getLogger('urllib3').setLevel(logging.ERROR)

class FypptSpider(scrapy.Spider):
    name = 'fyptt_spider'
    start_urls = ['https://fyptt.to']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    # 初始化下载视频的计数器
    video_download_count = 0
    
    def parse(self, response):
        # 获取总页数
        page_number = response.css('ul.page-numbers li:nth-last-child(2) a::text').get()
        page_number = 1  # 暂时设置为1页,可以根据需要修改
        print(f"找到{page_number}页数据.")
        # 遍历每一页
        for index in range(1, page_number + 1):
            yield scrapy.Request(
                url=f"https://fyptt.to/page/{index}",
                callback=self.get_pages,
                cb_kwargs={"index": index}
            )

    def get_pages(self, response, index):
        # 获取当前页面所有视频的URL
        urls = response.css("h3.fl-post-grid-title a::attr('href')").getall()
        print(f"第{index}页，找到{len(urls)}个视频")
        # 遍历每个视频URL
        for video_index, url in enumerate(urls):
            yield scrapy.Request(
                url=url,
                callback=self.get_video,
                cb_kwargs={"index": index, "video_index": video_index}
            )

    def get_video(self, response, index, video_index):
        # 解析视频ID和标题
        parsed_url = urlparse(response.url)
        id, title = parsed_url.path.split('/')[1:3]
        name = validateTitle(f"[{id}]{title}")
        file = Path(r"V:\【fyptt】") / f"{name}.mp4"

        # 检查文件是否已存在
        if file.exists():
            # print(f"第{index}页 第{video_index + 1}个视频 {name} 已存在")
            return

        # 提取视频URL并下载
        video_url = self.extract_video_url(response)
        if download_video(video_url, response.url, file):
            print(f"第{index}页 第{video_index + 1}个视频 {name} 下载成功")
            self.video_download_count += 1
        else:
            print(f"第{index}页 第{video_index + 1}个视频 {name} 下载失败")
            file.unlink(missing_ok=True)
    
    def closed(self, reason):
        print(f"爬虫已完成。总共下载了 {self.video_download_count} 个视频。")

    @staticmethod
    def extract_video_url(response):
        # 从iframe中提取视频URL
        parsed_url = urlparse(response.css("iframe::attr(src)").get())
        params = parse_qs(parsed_url.query)
        return f"https://stream.fyptt.to/{params['fileid'][0]}.mp4"

if __name__ == "__main__":
    # 创建并启动爬虫进程
    process = CrawlerProcess(settings=scrapy_settings)
    process.crawl(FypptSpider)
    process.start()
