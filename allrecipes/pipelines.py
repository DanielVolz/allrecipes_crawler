# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import logging
import pymongo


class MongoPipeline(object):
    collection_name = 'recipes_vegetarian'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.ids_seen = set()

    @classmethod
    def from_crawler(cls, crawler):
        # pull in information from settings.py
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        # initializing spider
        # opening db connection
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        # clean up when spider is closed
        self.client.close()

    def process_item(self, item, spider):
        # Filter Items with the same 'id'
        if item['id'] in self.ids_seen:
            logging.debug("Duplicate item found: "+str(item['id']))
        else:
            self.ids_seen.add(item['id'])
            self.db[self.collection_name].insert(dict(item))
            logging.debug("Post added to MongoDB reciepe_name: "+item['name'] + " id: " + str(item['id']))
