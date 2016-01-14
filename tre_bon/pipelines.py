#!/usr/bin/env python
# coding=utf-8
# -*- coding: utf-8 -*-
# Author: Tarek/ Araby
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

#import pymongo
import re
import pymysql
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from datetime import datetime
import sys
from bs4 import BeautifulSoup
import requests
import pickle
import re

reload(sys)
sys.setdefaultencoding('utf8')



class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
    	for key in item:
		if (key == 'image'  or key=='preview_image' or key=='media_url' ) and item[key]!='':
            		yield scrapy.Request(item[key].strip())

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        for key in item:
        	if(key == 'image'  or key=='preview_image' or key=='media_url') and len(image_path)!=0:
        		item[key] = 'images/articles/'+image_path[0]
        return item
class AccountImagePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
    	yield scrapy.Request(item['account_image'].strip())

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        item['account_image'] = 'images/articles/'+image_path[0]
        return item
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
		self.datedict.setdefault(10)


	def process_item(self, item, spider):


		if item['src']!='twitter' and item['type'] != 'article':
			return item

		for key in item:

			# fixing => removing trailing spaces, lowercasing and encoding (for arabic tags)
			# fixing tags
			if key == 'tags' and item['tags']!=' ' and not item['tags']:
				for count,tag in enumerate(item['tags']):
					item['tags'][count] = str(tag.encode('utf8')).strip()
				continue
			if key=='title' or key=='summary':
				item[key] = BeautifulSoup(item[key]).get_text()
				item[key] = item[key].encode('utf-8')
				continue
			# fixing all textual attributes


			if isinstance(item[key],str): item[key] = item[key].strip()

			# encoding textual attributes, date again in case of arabic since it contains months and days in alphabets
			if key in ['title','summary','content','date']:
				try:
					item[key] = str(item[key].encode('utf8')).strip()
				except:
					item[key] = str(item[key]).strip()

			#item[key] = re.sub( '\s+', ' ', item[key])


		'''
		Check for images link before adding the image downloader
		if item['type']=='article' :
			if item['image']!='':
				r = requests.post(item['image'].strip())
		        if r.status_code != 200:
		        	item['image'] = ''
		if item['type']!='livescore' and item['account_image']!='':
		    r = requests.post(item['account_image'].strip())
		    if r.status_code != 200:
		        item['account_image'] = ''
		'''
		# converting different (customized) date formats to datetime python format
		try:
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
				item['date'] = datetime.fromtimestamp(int(date))

			elif item['src'] == "fifa":
				item['date'] = datetime.now()


			elif item['src'] == "filgoal":
				date = str(item['date']).split()
				day = date[2]
				month = self.datedict[date[3]]
				year = date[5]
				time = date[7]
				date = "%s-%s-%s %s" % (year,month,day,time)
				item['date'] = datetime.strptime(date,  "%Y-%m-%d %H:%M")


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

			elif item['src'] == 'teamtalk':
				date = str(item['date']).split(" ")
				day = re.sub('[a-zA-Z]','',date[0])
				month = self.datedict[date[1]]
				year = date[2]
				dateformatted = "%s-%s-%s %s" % (year,month,day,date[3])
				item['date'] = datetime.strptime(dateformatted,  "%Y-%m-%d %H:%M")

			elif item['src'] == 'whoscored':
				date = item['date'].split(' ')
				month = self.datedict[date[0]]
				dateformatted = "%s-%s-%s %s" % (date[2],month,date[1],date[3])
				item['date'] = datetime.strptime(dateformatted,  "%Y-%m-%d %H:%M")
			elif item['src']=='facebook':
				item['date'] = re.sub(r'\+[0-9]{4}','',item['date'])
				item['date'] = datetime.strptime(item['date'] ,  "%Y-%m-%dT%H:%M:%S")
		except:
			item['date'] = datetime.now()
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


		if item['src']!='twitter' and item['type'] != 'video':
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
		if 'url' not in item:
			return item
		if item['url'] in self.urls_seen:
			raise DropItem("Duplicate item found, ignored by duplicate pipeline")
		else:
			self.urls_seen.add(item['url'])
			return item
# read items, check if they are not already in db, then add them.
class MySQLArticlesPipeline(object):

	def __init__(self):
		self.db =  pymysql.connect(host=settings['MYSQLDB_SERVER'], # your host, usually localhost
                     user=settings["MYSQLDB_USER"], # your username
                      passwd=settings["MYSQLDB_PWD"], # your password
                      db=settings["MYSQLDB_DB"]) # name of the data base
		self.db.set_charset('utf8')
		# you must create a Cursor object. It will let
		#  you execute all the queries you need
		self.cur = self.db.cursor()

	def process_item(self, item, spider):
		try:
			f = '%Y-%m-%d %H:%M:%S'
			item['date'] = item['date'].strftime(f)
		except:
			if 'date' in item:
				today = datetime.today()
				item['date'] = today.strftime(f) #workaround TODO needs to be fixed
		for key in item:
			try:
				item[key] = str(item[key])
				item[key] = item[key].replace('"','').replace("'","")
			except :
				try:
					item[key] = ' '.join(item[key])
				except:
					print key

		if item['src']=='livescore':
			item['matchDateTime'] = datetime.strptime(item['matchDateTime'],  "%d-%m-%Y %H:%M")
			f = '%Y-%m-%d %H:%M:%S'
			item['matchDateTime'] = item['matchDateTime'].strftime(f)
			if item['localTeamScore']=='?':
				item['localTeamScore'] = '0'
			if item['visitorTeamScore']== '?':
				item['visitorTeamScore'] = '0'

			self.cur.execute('INSERT INTO livescores(competition,competitionLogo,visitorTeam,visitorTeamLogo,localTeam,localTeamLogo,visitorTeamScore,localTeamScore,matchDateTime) VALUES("'+item['competition']+'","'+item['competitionLogo']+'","'+item['visitorTeam']+'","'+item['visitorTeamLogo']+'","'+item['localTeam']+'","'+item['localTeamLogo']+'",'+item['visitorTeamScore']+','+item['localTeamScore']+',"'+item['matchDateTime']+'")')
		else:
			#self.cur.execute('SELECT itemIndex FROM articles WHERE src=%s order by date desc LIMIT 1;',(item['src']))
			#itemIndex = self.cur.fetchall()
			#if len(itemIndex)>0:
			#	item['itemIndex'] = str(int(itemIndex[0][0])+1)
			#else:
			#	item['itemIndex'] = "0"
			if  item['src']=='twitter':
				self.cur.execute('INSERT INTO twitter (account_img,itemIndex,text,account,tags,url,media_url,retweets,lang,favs,tweet_id,date) VALUES("'+item['account_image']+'","'+item['itemIndex']+'","'+item['text']+'","'+item['account']+'","'+item['tags']+'","'+item['url']+'","'+item['media_url']+'","'+item['retweets']+'","'+item['lang']+'","'+item['favs']+'","'+item['tweet_id']+'","'+item['date']+'")')
			elif item['src']=='instagram':
				self.cur.execute('INSERT INTO instagram (account_img,itemIndex,caption,account,tags,url,img_vid_src,likes,lang,media_id,date) VALUES("'+item['account_image']+'","'+item['itemIndex']+'","'+item['caption']+'","'+item['account']+'","'+item['tags']+'","'+item['url']+'","'+item['img_vid_src']+'","'+item['likes']+'","'+item['lang']+'","'+item['media_id']+'","'+item['date']+'")')
			elif item['type']=='video':
				self.cur.execute('INSERT INTO videos (account_img,itemIndex,title,url,lang,preview_image,embed_code,embed_url,channel,date) VALUES("'+item['account_image']+'","'+item['itemIndex']+'","'+item['title']+'","'+item['url']+'","'+item['lang']+'","'+item['preview_image']+'","'+item['embed_code']+'","'+item['embed_url']+'","'+item['channel']+'","'+item['date']+'")')
			elif item['type']=='article':
				self.cur.execute('INSERT INTO articles (postId,account_img,src,itemIndex,title,url,image,summary,tags,lang,content,date) VALUES("'+item['postId']+'","'+item['account_image']+'","'+item['src']+'","'+item['itemIndex']+'","'+item['title']+'","'+item['url']+'","'+item['image']+'","'+item['summary']+'","'+item['tags']+'","'+item['lang']+'","'+item['content']+'","'+item['date']+'")')
			elif item['type']=='team_logo':
				self.cur.execute('INSERT INTO teamlogos(name,image) VALUES("'+item['name']+'","'+item['image']+'")')

		self.db.commit()
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

	def process_item(self, item, spider):
		if self.feed_items.find({'url': item['url']}).count() == 0:
			self.feed_items.insert(dict(item))
			return item
		else:
			spider.close_down = True
