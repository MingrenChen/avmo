# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json
from scrapy.utils.misc import md5sum
from scrapy.pipelines.images import ImagesPipeline
import scrapy

class AvmoPipeline(object):

    def __init__(self):
        self.f2 = open('avmo.json', 'wb')

    def process_item(self, item, spider):
        # print(item["pic"])
        content = json.dumps(dict(item), ensure_ascii=False)
        self.f2.write(content.encode("utf-8"))
        return item

    def close_spider(self, spider):
        self.f2.close()


class BtsoPipeline(object):
    def process_item(self,item,spider):
        id_ = item['id_']
        with open(r"/home/mingren/project/avmo/avmo/img/" + id_ + ".txt", 'a') as f:
            f.write(item['title'] + '\n')
            f.write(item['magnet'] + '\n')
        return item

# class ImgPipeline(ImagesPipeline):
#     def get_media_requests(self, item, info):
#         img_url = item["pic"]
#         self.citem = item
#         yield scrapy.Request(img_url)
#
#     def item_completed(self, results, item, info):
#         return item
#
#     def image_key(self, url):
#         name = self.citem['id_'] + " " + self.citem['name']
#         if len(name) < 80:
#             image_guid = name
#         else:
#             image_guid = self.citem['id_']
#         return 'full/%s' % (image_guid)
