# -*- coding: utf-8 -*-
import scrapy, re, os, sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
import items

class BtsoSpider(scrapy.Spider):
    name = 'btso'
    allowed_domains = ['btso.pw']
    start_urls = []
    with open(r'/home/mingren/project/avmo/avmo/spiders/urls.txt', 'r') as u:
        for line in u.readlines():
            line = line.strip()
            start_urls.append(line)
    custom_settings = {
        'ITEM_PIPELINES': {
            'avmo.pipelines.BtsoPipeline': 300,
        }
    }

    def parse(self, response):
        if response.xpath("//div[@class=\"data-list\"]"):
            for each in response.xpath("//div[@class=\"data-list\"]/div[@class=\"row\"]"):
                url = each.xpath("a/@href").extract()[0]
                yield scrapy.Request(url, callback=self.parse_magnet)

    def parse_magnet(self,response):
        title = response.xpath("/html/body/div[2]/h3/text()").extract()[0]
        cgroups = re.findall("[a-zA-Z]{2,5}-{0,3}\d{2,4}", title)
        item = items.MagnetItem()
        if len(cgroups) == 1:
            item['id_'] = re.search('[a-zA-Z]{2,5}', cgroups[0]).group(0) + "-" + re.search('\d{3,5}', cgroups[0]).group(0)
            item['magnet'] = response.xpath('//*[@id=\"magnetLink\"]/text()').extract()[0]
            item['title'] = title
            yield item
