# -*- coding: utf-8 -*-
import scrapy
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
import items


class JavbusSpider(scrapy.Spider):
    name = 'avmoo'
    allowed_domains = ['https://avio.pw/cn']
    start_urls = ['https://avio.pw/cn/']

    def parse(self, response):
        for each in response.xpath("//a[@class=\"movie-box\"]"):
            item = items.AvmoItem()
            id_ = each.xpath("div[@class=\"photo-info\"]/span/date/text()").extract()[0]
            name = each.xpath("div[@class=\"photo-info\"]/span/text()").extract()[0]
            pic = each.xpath("div[@class=\"photo-frame\"]/img[@src]").extract()[0]
            item["id_"] = id_
            item["name"] = name
            item["pic"] = pic
            yield item