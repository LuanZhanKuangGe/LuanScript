# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy import Request
from scrapy.pipelines.files import FilesPipeline


class Rule34XxxPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        urls = ItemAdapter(item).get(self.files_urls_field, [])
        name = urls.split('?')[1]
        urls = urls.split('?')[0]
        return [Request(urls, meta={'name': name})]
        # return [Request(u) for u in urls]

    def file_path(self, request, response=None, info=None):

        if len(request.meta['name'].split('_')) > 2:
            return '%s.mp4' % request.meta['name']
        else:
            name = request.meta['name'].split('_')[0] + "/" + request.meta['name']
            return '%s.mp4' % name

