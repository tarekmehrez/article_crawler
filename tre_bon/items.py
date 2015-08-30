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
	date = scrapy.Field()
	time = scrapy.Field()
	summary = scrapy.Field()
	tags = scrapy.Field()