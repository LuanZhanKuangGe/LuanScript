from scrapy import cmdline



cmdline.execute("scrapy crawl main -a artist=all".split())
