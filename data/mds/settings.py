# -*- coding: utf-8 -*-

# Scrapy settings for mds project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'mds'

SPIDER_MODULES = ['mds.spiders']
NEWSPIDER_MODULE = 'mds.spiders'

ITEM_PIPELINES = ['mds.pipelines.JsonWithEncodingPipeline']
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'mds (+http://www.yourdomain.com)'
