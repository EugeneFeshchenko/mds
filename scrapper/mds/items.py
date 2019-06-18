# -*- coding: utf-8 -*-

import scrapy


class MdsItem(scrapy.Item):
    author = scrapy.Field()
    name = scrapy.Field()
    links = scrapy.Field()
    number = scrapy.Field()
