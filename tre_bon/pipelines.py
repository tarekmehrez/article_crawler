# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class TreBonPipeline(object):
#     def process_item(self, item, spider):
#         return item


import pymongo

from scrapy.conf import settings


class MongoDBPipeline(object):

    def __init__(self):
		connection = pymongo.MongoClient(
			settings['MONGODB_SERVER'],
			settings['MONGODB_PORT']
		)
		db = connection[settings['MONGODB_DB']]
		self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
		valid = True

		self.collection.insert(dict(item))
		# log.msg("Question added to MongoDB database!", level=log.DEBUG, spider=spider)
		return item