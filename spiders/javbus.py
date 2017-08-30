# -*- coding: utf-8 -*-
import scrapy
import os
import sys
import re
import urllib.parse
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
import items


class JavbusSpider(scrapy.Spider):
    name = 'avmoo'
    allowed_domains = ['www.ja14b.com']
    start_urls = ['http://www.ja14b.com/cn/vl_genre.php?g=cu']

    def parse(self, response):
        for av in response.xpath("//div[@class=\"video\"]"):
            url = urllib.parse.urljoin('http://www.ja14b.com/cn/', av.xpath("a/@href").extract()[0])
            yield scrapy.Request(url, callback=self.parse_movie)

        next_page = response.xpath("//*[@class=\"page next\"]")
        has_next_page = next_page != []
        if has_next_page:
            next_page_url = "http://www.ja14b.com" + response.xpath("//*[@id=\"rightcolumn\"]/div[3]/a[9]/@href").extract()[0]
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_movie(self, response):
        title = response.xpath("//*[@id=\"video_title\"]/h3/a/text()").extract()[0]
        item = items.AvmoItem()

        id_ = re.search("[a-zA-Z]{2,5}-?\d{2,5}",title).group(0)
        name = title[len(id_)+1:]
        pic = "http:" + response.xpath("//*[@id=\"video_jacket_img\"]/@src").extract()[0]

        item["url"] = response.url
        item["id_"] = id_
        item["name"] = name
        item["pic"] = pic
        yield item

