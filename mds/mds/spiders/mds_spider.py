# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from mds.items import MdsItem


class MdsSpider(scrapy.Spider):
    name = "mds_spider"
    allowed_domains = ["http://mds-club.ru", "mds-club.ru"]
    start_urls = [
        "http://mds-club.ru/cgi-bin/index.cgi?r=84&lang=rus/catalog",
        "http://mds-club.ru/cgi-bin/index.cgi?r=84&lang=rus&filter=0&article=0&sortby=20&posits=50&search=",
        "http://mds-club.ru/cgi-bin/index.cgi?r=84&lang=rus&filter=0&article=0&sortby=20&posits=100&search=",
        "http://mds-club.ru/cgi-bin/index.cgi?r=84&lang=rus&filter=0&article=0&sortby=20&posits=150&search=",
        "http://mds-club.ru/cgi-bin/index.cgi?r=84&lang=rus&filter=0&article=0&sortby=20&posits=200&search=",
        "http://mds-club.ru/cgi-bin/index.cgi?r=84&lang=rus&filter=0&article=0&sortby=20&posits=250&search=",
        "http://mds-club.ru/cgi-bin/index.cgi?r=84&lang=rus&filter=0&article=0&sortby=20&posits=300&search=",
        "http://mds-club.ru/cgi-bin/index.cgi?r=84&lang=rus&filter=0&article=0&sortby=20&posits=350&search=",
        "http://mds-club.ru/cgi-bin/index.cgi?r=84&lang=rus&filter=0&article=0&sortby=20&posits=400&search=",
        "http://mds-club.ru/cgi-bin/index.cgi?r=84&lang=rus&filter=0&article=0&sortby=20&posits=450&search=",
        "http://mds-club.ru/cgi-bin/index.cgi?r=84&lang=rus&filter=0&article=0&sortby=20&posits=500&search=",
        "http://mds-club.ru/cgi-bin/index.cgi?r=84&lang=rus&filter=0&article=0&sortby=20&posits=550&search=",
        "http://mds-club.ru/cgi-bin/index.cgi?r=84&lang=rus&filter=0&article=0&sortby=20&posits=600&search=",
        "http://mds-club.ru/cgi-bin/index.cgi?r=84&lang=rus&filter=0&article=0&sortby=20&posits=650&search=",
        "http://mds-club.ru/cgi-bin/index.cgi?r=84&lang=rus&filter=0&article=0&sortby=20&posits=700&search=",
        "http://mds-club.ru/cgi-bin/index.cgi?r=84&lang=rus&filter=0&article=0&sortby=20&posits=750&search=",
        "http://mds-club.ru/cgi-bin/index.cgi?r=84&lang=rus&filter=0&article=0&sortby=20&posits=800&search=",
        "http://mds-club.ru/cgi-bin/index.cgi?r=84&lang=rus&filter=0&article=0&sortby=20&posits=850&search=",
        "http://mds-club.ru/cgi-bin/index.cgi?r=84&lang=rus&filter=0&article=0&sortby=20&posits=900&search=",
        "http://mds-club.ru/cgi-bin/index.cgi?r=84&lang=rus&filter=0&article=0&sortby=20&posits=950&search=",
        "http://mds-club.ru/cgi-bin/index.cgi?r=84&lang=rus&filter=0&article=0&sortby=20&posits=1000&search=",
        "http://mds-club.ru/cgi-bin/index.cgi?r=84&lang=rus&filter=0&article=0&sortby=20&posits=1050&search=",
    ]


    def parse(self, response):

        for row in response.css('#catalogtable tbody tr'):
            item = MdsItem()
            item['author'] =  row.css('td:nth-child(2) a::text').extract()[0]
            item['name'] = row.css('td:nth-child(3) a::text').extract()[0]
            item['number'] = int(row.css('td:nth-child(1) a:nth-child(1)::text').extract()[0])
            link = row.xpath('td[position()=2]/a/@href').extract()[0]
            yield Request(link, meta={'item': item}, callback=self.parse_job)

    def parse_job(self, response):
        item = response.request.meta['item']
        href = response.css('#catalogtable tbody tr:nth-child(1) td:nth-child(4)')
        href = href.xpath('a/@href').extract()[0]
        item['link'] = href
        item['size'] = response.css('#catalogtable tbody tr:nth-child(1) td:nth-child(5)::text').extract()[0]
        return item
