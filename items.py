# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AvmoItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pic = scrapy.Field()
    url = scrapy.Field()
    id_ = scrapy.Field()

class MagnetItem(scrapy.Item):
    id_ = scrapy.Field()
    magnet = scrapy.Field()
    title = scrapy.Field()