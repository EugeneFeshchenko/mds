# -*- coding: utf-8 -*-


import json
import codecs
from scrapy.xlib.pydispatch import dispatcher 
from scrapy import signals


class JsonWithEncodingPipeline(object):

    def __init__(self):
        self.trans = '['
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + ", "
        self.trans += line
        return item

    def spider_closed(self, spider):
        self.trans = self.trans[:-2]+']'
        items = json.loads(self.trans)
        items = sorted(items, key=lambda val:val['number'])
        self.trans = json.dumps(items, ensure_ascii=False)

        self.file = codecs.open('scraped.json', 'w+', encoding='utf-8')
        self.file.write(self.trans)
        self.file.close()
