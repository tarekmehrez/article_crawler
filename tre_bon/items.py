# Author: Tarek

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
	title = scrapy.Field()
	url = scrapy.Field()
	image = scrapy.Field()
	date = scrapy.Field()
	summary = scrapy.Field()
	tags = scrapy.Field()
	src = scrapy.Field()
	lang = scrapy.Field()
	content = scrapy.Field()
	type = scrapy.Field()

class VideoItem(scrapy.Item):
	title = scrapy.Field()
	url = scrapy.Field()
	date = scrapy.Field()
	src = scrapy.Field()
	channel = scrapy.Field()
	lang = scrapy.Field()
	preview_image = scrapy.Field()
	embed_code = scrapy.Field()
	embed_url = scrapy.Field()
	type = scrapy.Field()

class InstagramItem(scrapy.Item):
	caption = scrapy.Field()
	date = scrapy.Field()
	src = scrapy.Field()
	account = scrapy.Field()
	tags = scrapy.Field()
	url = scrapy.Field()
	type = scrapy.Field()
	img_vid_src = scrapy.Field()
	likes = scrapy.Field()
	lang = scrapy.Field()
	media_id = scrapy.Field()

class TwitterItem(scrapy.Item):
	text = scrapy.Field()
	date = scrapy.Field()
	src = scrapy.Field()
	account = scrapy.Field()
	tags = scrapy.Field()
	url = scrapy.Field()
	media_url = scrapy.Field()
	retweets = scrapy.Field()
	lang = scrapy.Field()
	favs = scrapy.Field()
	tweet_id = scrapy.Field()