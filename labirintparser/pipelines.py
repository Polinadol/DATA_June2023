# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient

class LabirintparserPipeline:
    def __init__(self):
        client=MongoClient('localhost',27017)
        self.mongo_base=client.labirints
    def process_item(self, item, spider):
        collection = self.mongo_base['labirints']

        collection.insert_one(item)  # Добавляем в базу данных
        return item



class LabirintphotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for img in item['photos']:
            try:
                yield scrapy.Request(img)
            except Exception as e:
                print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    # def file_path(self, request, response=None, info=None, *, item=None):
    #
    #     return
