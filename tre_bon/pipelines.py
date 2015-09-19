# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import re
import logging
import sys

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from datetime import datetime

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
							"Jan":		1,
							"Feb":		2,
							"Mar":		3,
							"Apr":		4,
							"May":		5,
							"Jun":		6,
							"Jul":		7,
							"Aug":		8,
							"Sep":		9,
							"Oct":		10,
							"Nov":		11,
							"Dec":		12,
							}

	def process_item(self, item, spider):

		if item['type'] != 'article':
			return item

		for key in item:

			# fixing => removing trailing spaces, lowercasing and encoding (for arabic tags)
			# fixing tags
			if key == 'tags':
				for count,tag in enumerate(item['tags']):
					item['tags'][count] = str(tag.strip().lower().encode('utf8'))
				continue

			# fixing all textual attributes


			if isinstance(item[key],str): item[key] = item[key].strip()

			# encoding textual attributes, date again in case of arabic since it contains months and days in alphabets
			if key in ['title','summary','content','date']:
				try:
					item[key] = str(item[key].encode('utf8'))
				except:
					item[key] = str(item[key])

			item[key] = re.sub( '\s+', ' ', item[key])


		# converting different (customized) date formats to datetime python format
		if item['src'] == 'bein':
			date = item['date'].split('+')[0]
			date = re.sub('[a-zA-Z]',' ',date)
			item['date'] = datetime.strptime(date,  "%Y-%m-%d %H:%M:%S")

		elif item['src'] == 'bleacher_report':
			date = item['date']
			date = re.sub('[a-zA-Z]',' ',date).strip()
			item['date'] = datetime.strptime(date,  "%Y-%m-%d %H:%M:%S")

		elif item['src'] == "cairokora":

			date = item['date'].split(",")[1]

			day = date.split(" ")[0]
			month = self.datedict[date.split(" ")[1]]
			year = date.split(" ")[2]
			time = date.split(" ")[4]
			date = "%s-%s-%s %s" % (year,month,day,time)
			item['date'] = datetime.strptime(date,  "%Y-%m-%d %H:%M")

		elif item['src'] == "espnfc":
			date = item['date']
			item['date'] = datetime.fromtimestamp(int(date) / 1e3)

		elif item['src'] == "fifa":
			item['date'] = datetime.now()

		elif item['src'] == "goal":
			if item['lang'] == 'en':
				date = item['date'].split(",")[1].strip()
				day = date.split(" ")[1]
				month = self.datedict[date.split(" ")[0]]

				date = item['date'].split(",")[2].strip()
				year = date[:4]
				time = date[4:]
			else:
				date = item['date'].split("،")[1].strip()
				day = date.split(" ")[0]
				month = self.datedict[date.split(" ")[1]]

				date = item['date'].split("،")[2].strip()

				year = date[:4]
				time = date[4:].split(" ")[0]

			date = "%s-%s-%s %s" % (year,month,day,time)
			item['date'] = datetime.strptime(date,  "%Y-%m-%d %H:%M")


		elif item['src'] == 'greatgoals':
			date = item['date'].strip()

			month = self.datedict[date.split(" ")[0]]
			day = date.split(" ")[1].split(",")[0].strip()
			year = date.split(",")[1].strip()
			date = "%s-%s-%s %s" % (year,month,day,datetime.now().strftime('%H:%M:%S'))
			item['date'] = datetime.strptime(date,  "%Y-%m-%d %H:%M:%S")


		elif item['src'] == 'talksport':

			date = item['date']
			day = date.split(",")[1].strip().split(" ")[1]
			month = self.datedict[date.split(",")[1].strip().split(" ")[0]]
			year = item['date'].split(",")[2].strip()
			date = "%s-%s-%s %s" % (year,month,day,datetime.now().strftime('%H:%M:%S'))
			item['date'] = datetime.strptime(date,  "%Y-%m-%d %H:%M:%S")


		elif item['src'] == 'hihi2':
			date = item['date'].replace('ص','AM').replace('م','PM').strip()
			if date.split(' ')[3] == 'PM':
				old = date.split(' ')[2]
				old_arr = date.split(' ')[2].split(":")

				if old_arr[0] != '12':
					new = int(old_arr[0]) + 12
					result = ':'.join([str(new),old_arr[1]])
					date = date.replace(old,result)


			date = date.replace("AM","").replace("PM","").replace('- ','').strip()
			item['date'] = datetime.strptime(date,  "%Y/%m/%d %H:%M")

		elif item['src'] == 'skysports':
			date = item['date'].replace('am',' AM').replace('pm',' PM').strip()
			if date.split(' ')[2] == 'PM':
				old = date.split(' ')[1]
				old_arr = date.split(' ')[1].split(":")

				if old_arr[0] != '12':
					new = int(old_arr[0]) + 12
					result = ':'.join([str(new),old_arr[1]])
					date = date.replace(old,result)

			date = date.replace("AM","").replace("PM","").replace('- ','').strip()
			item['date'] = datetime.strptime(date,  "%d/%m/%y %H:%M")

		elif item['src'] == 'yallakora':
			if 'date' in item:
				date = item['date'].strip()

				day = date.split(" ")[0]

				month = self.datedict[date.split(" ")[1]]
				year = date.split(" ")[2]

				time = ' '.join(date.split(" ")[4:]).replace('ص','AM').replace('م','PM').strip()

				date = "%s-%s-%s %s" % (year,month,day,time)

				if date.split(' ')[2] == 'PM':
					old = date.split(' ')[1]
					old_arr = date.split(' ')[1].split(":")
					if old_arr[0] != '12':
						new = int(old_arr[0]) + 12
						result = ':'.join([str(new),old_arr[1]])
						date = date.replace(old,result)

				date = date.replace("AM","").replace("PM","").strip()
				item['date'] = datetime.strptime(date,  "%Y-%m-%d %H:%M")

			else:
				item['date'] = datetime.now()
		elif item['src'] == 'korabia':

			date_arr = item['date'].strip().split(" ")
			day = date_arr[1]
			month = self.datedict[date_arr[2]]
			year = date_arr[3]

			time = date_arr[5]
			if date_arr[6] == 'PM':
				time_arr = time.split(":")
				if time_arr[0] != '12':

					new_time = str(12 + int(time_arr[0])) + ":" + time_arr[1]
					time = new_time

			date = "%s-%s-%s %s" % (year,month,day,time)
			item['date'] = datetime.strptime(date,  "%Y-%m-%d %H:%M")

		# in case we failed to find any date for the article, save the article with the current datetime
		if 'date' not in item:
			item['date'] = datetime.now()
		return item


class VideoPipeline(object):

	def __init__(self):
		self.datedict = {	"Jan":		1,
							"Feb":		2,
							"Mar":		3,
							"Apr":		4,
							"May":		5,
							"Jun":		6,
							"Jul":		7,
							"Aug":		8,
							"Sep":		9,
							"Oct":		10,
							"Nov":		11,
							"Dec":		12,
							}

	def process_item(self, item, spider):


		if item['type'] != 'video':
			return item

		if 'youtube' in item['src']:

			date = item['date'].strip()
			date_arr = date.split(' ')

			month = self.datedict[date_arr[0]]

			day = date_arr[1].replace(',','')

			year = date_arr[2]

			date = "%s-%s-%s %s" % (year,month,day,datetime.now().strftime('%H:%M'))
			item['date'] = datetime.strptime(date,  "%Y-%m-%d %H:%M")


		elif 'dailymotion' in item['src']:

			date_arr = item['date'].strip().split("/")

			date = "%s-%s-%s %s" % (date_arr[2],date_arr[0],date_arr[1],datetime.now().strftime('%H:%M'))
			item['date'] = datetime.strptime(date,  "%Y-%m-%d %H:%M")

		return item


# yet another duplicates filer, double safety
class DuplicatesPipeline(object):

	def __init__(self):
		self.urls_seen = set()

	def process_item(self, item, spider):
		if item['url'] in self.urls_seen:
			raise DropItem("Duplicate item found, ignored by duplicate pipeline")
		else:
			self.urls_seen.add(item['url'])
			return item


# read items, check if they are not already in db, then add them.
class MongoArticlesPipeline(object):

	def __init__(self):
		connection = pymongo.MongoClient(
			settings['MONGODB_SERVER'],
			settings['MONGODB_PORT']
		)
		db = connection[settings['MONGODB_DB']]
		self.feed_items = db[settings['MONGODB_COLLECTION']]
		self.logger = logging.getLogger()

	def process_item(self, item, spider):
		if self.feed_items.find({'url': item['url']}).count() == 0:
			self.feed_items.insert(dict(item))
			return item
		else:
			spider.close_down = True