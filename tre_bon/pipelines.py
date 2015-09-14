# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import re


from scrapy.conf import settings


class ArticlePipeline(object):
	def __init__(self):
		self.datedict = {	'يناير':	1,
							'فبراير':	2,
							'مارس':		3,
							'ابريل':	4,
							'مايو':		5,
							'يونيو':	6,
							'يوليو':	7,
							'أغسطس':	8,
							'سبتمبر': 	9,
							'أكتوبر': 	10,
							'نوفمبر': 	11,
							'ديسمبر': 	12,
							"January":	1,
							"February":	2,
							"March":	3,
							"April":	4,
							"May":		5,
							"June":		6,
							"July":		7,
							"August":	8,
							"September":9,
							"October":	10,
							"November":	11,
							"December":	12,
							}

	def process_item(self, item, spider):

		item['type'] = "article"

		for key in item:

			if key == 'tags':
				for count,tag in enumerate(item['tags']):
					item['tags'][count] = str(tag.strip().lower().encode('utf8'))
				continue

			if isinstance(item[key],str): item[key] = item[key].strip()

			if key in ['title','summary','content','datetime']:
				try:
					item[key] = str(item[key].encode('utf8'))
				except:
					item[key] = str(item[key])

			item[key] = re.sub( '\s+', ' ', item[key])

		if item['src'] == "cairokora":

			date = item['datetime'].split(",")[1]

			day = date.split(" ")[0]
			month = self.datedict[date.split(" ")[1]]
			year = date.split(" ")[2]
			time = date.split(" ")[4]
			item['datetime'] = "%s-%s-%s %s" % (year,month,day,time)

		if item['src'] == "goal":
			if item['lang'] == 'en':
				date = item['datetime'].split(",")[1].strip()
				day = date.split(" ")[1]
				month = self.datedict[date.split(" ")[0]]

				date = item['datetime'].split(",")[2].strip()

				year = date[:4]
				time = date[4:]
			else:
				date = item['datetime'].split("،")[1].strip()
				day = date.split(" ")[0]
				month = self.datedict[date.split(" ")[1]]

				date = item['datetime'].split("،")[2].strip()

				year = date[:4]
				time = date[4:].split(" ")[0]

			item['datetime'] = "%s-%s-%s" % (year,month,day,time)


		if item['src'] == 'greatgoals':
			date = item['datetime'].strip()

			month = self.datedict[date.split(" ")[0]]
			day = date.split(" ")[1].split(",")[0].strip()
			year = date.split(",")[1].strip()
			item['datetime'] = "%s-%s-%s" % (year,month,day)


		if item['src'] == 'talksport':

			date = item['datetime']
			day = date.split(",")[1].strip().split(" ")[1]
			month = self.datedict[date.split(",")[1].strip().split(" ")[0]]
			year = item['datetime'].split(",")[2].strip()
			item['datetime'] = "%s-%s-%s" % (year,month,day)


		if item['src'] == 'hihi2':
			item['datetime'] = item['datetime'].replace('ص','AM').replace('م','PM').strip()

		if item['src'] == 'skysports':
			item['datetime'] = item['datetime'].replace('am',' AM').replace('pm',' PM').strip()


		if item['src'] == 'yallakora' and 'datetime' in item:
			date = item['datetime'].strip()

			day = date.split(" ")[0]

			month = self.datedict[date.split(" ")[1]]
			year = date.split(" ")[2]

			time = ' '.join(date.split(" ")[4:]).replace('ص','AM').replace('م','PM').strip()

			item['datetime'] = "%s-%s-%s %s" % (year,month,day,time)

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