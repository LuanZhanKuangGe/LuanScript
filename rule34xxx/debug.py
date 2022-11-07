from scrapy import cmdline
import winsound

cmdline.execute("scrapy crawl main -a artist=all".split())

duration = 5000  # 持续时间以毫秒为单位，这里是5秒
freq = 440  # Hz
winsound.Beep(freq, duration)
