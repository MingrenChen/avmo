# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import dill
import json


class AvmoPipeline(object):

    def __init__(self):
        self.items = set()
        self.f = open("avmo.pickle", "wb")
        self.f1 = open("avmo.out", "w")
        self.f2 = open('avmo.json', 'wb')

    def process_item(self, item, spider):
        # print(item["pic"])
        self.f1.write(str(item))
        content = json.dumps(dict(item), ensure_ascii=False)
        self.f2.write(content.encode("utf-8"))
        return item
        # self.items.add(check.Av(item['url'],item['pic'],item['name'],item['id_']))


    def close_spider(self,spider):
        dill.dump(self.items, self.f)
        print(len(self.items))
        self.f.close()
        self.f1.close()
        self.f2.close()


# class ImgPipeline(ImagesPipeline):
#     def get_media_requests(self, item, info):
#         img_url = item["pic"]
#         yield scrapy.Request("http:" + img_url)
#
#     def item_completed(self, results, item, info):
#         return item

    # def file_path(self, request, response=None, info=None):
    #     item = request.meta['item']
    #     filename = '{} {}.jpg'.format(item['id_'], item['name'])
    #     return filename