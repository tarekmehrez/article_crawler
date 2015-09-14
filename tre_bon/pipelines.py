# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import re


from scrapy.conf import settings


class ArticlePipeline(object):
	def process_item(self, item, spider):

		item['type'] = "article"

		for key in ['url','image','title','summary','content']:
			if key in item:
				item[key] = item[key].strip()

		if 'tags' in item:
			for count,tag in enumerate(item['tags']):
				item['tags'][count] = tag.strip().lower()


		if 'content' in item:
			item['content'] = re.sub( '\s+', ' ', item['content'])

		return item


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