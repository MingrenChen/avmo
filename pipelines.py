# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class AvmoPipeline(object):

    def __init__(self):
        self.f = open("avmoo_pipline.py","w")

    def process_item(self, item, spider):
        self.f.write(str(item))

    def close_spider(self,spider):
        self. f.close()