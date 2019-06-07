# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from mds.items import MdsItem


class MdsSpider(scrapy.Spider):
    name = "mds_spider"
    allowed_domains = ["mds-club.ru"]

    start_urls = [
        "http://mds-club.ru/cgi-bin/index.cgi?r=84&lang=rus&filter=0&article=0&sortby=20&posits=0",
    ]

    def parse(self, response):

        for row in response.css('#catalogtable tbody tr'):
            item = MdsItem()
            item['author'] = row.css('td:nth-child(2) a::text').extract_first()
            item['name'] = row.css('td:nth-child(3) a::text').extract_first()
            number = row.css('td:nth-child(1) a:nth-child(1)::text').extract_first()
            item['number'] = int(number) if number else None
            link = row.xpath('td[position()=2]/a/@href').extract_first()
            if link:
                yield Request(link, meta={'item': item}, callback=self.parse_job)

            next_page = response.css('#roller_active + div a::attr(href)').extract_first()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_job(self, response):
        item = response.request.meta['item']
        links = response.css('#catalogtable tbody tr td:nth-child(4) a::attr(href)').getall()
        item['links'] = ' || '.join(links)
        return item
