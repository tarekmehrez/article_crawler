# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TreBonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class GoalENItem(scrapy.Item):
	title = scrapy.Field()
	url = scrapy.Field()
	image = scrapy.Field()
	datetime = scrapy.Field()
	summary = scrapy.Field()
	tags = scrapy.Field()
	src = scrapy.Field()
	lang = scrapy.Field()

class ESPNItem(scrapy.Item):
	title = scrapy.Field()
	url = scrapy.Field()
	image = scrapy.Field()
	datetime = scrapy.Field()
	summary = scrapy.Field()
	tags = scrapy.Field()
	src = scrapy.Field()
	lang = scrapy.Field()

class TalkSportItem(scrapy.Item):
	title = scrapy.Field()
	url = scrapy.Field()
	image = scrapy.Field()
	datetime = scrapy.Field()
	summary = scrapy.Field()
	tags = scrapy.Field()
	src = scrapy.Field()
	lang = scrapy.Field()

class FifaENItem(scrapy.Item):
	title = scrapy.Field()
	url = scrapy.Field()
	image = scrapy.Field()
	datetime = scrapy.Field()
	summary = scrapy.Field()
	src = scrapy.Field()
	lang = scrapy.Field()

class BeinENItem(scrapy.Item):
	title = scrapy.Field()
	url = scrapy.Field()
	image = scrapy.Field()
	datetime = scrapy.Field()
	src = scrapy.Field()
	lang = scrapy.Field()

class GreatGoalsItem(scrapy.Item):
	title = scrapy.Field()
	url = scrapy.Field()
	image = scrapy.Field()
	datetime = scrapy.Field()
	src = scrapy.Field()
	lang = scrapy.Field()
	tags = scrapy.Field()