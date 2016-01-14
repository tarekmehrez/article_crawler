# Author: Tarek

import scrapy
import json
import urllib2

from lxml import etree
from tre_bon.items import ArticleItem
from datetime import datetime

class ESPNSpider(scrapy.Spider):
	name = 'espn'
	allowed_domains = ["espnfc.com"]
	start_urls=["http://www.espnfc.com/news"]
	itemCount = 1
	def parse(self, response):


		data = json.load(urllib2.urlopen("http://www.espnfc.com/api/feed?xhr=1&t=54&device=pc&limit=100&content=story&offset=0&key=espnfc-en-www-index-news-600"))
		articles = data['data']['features']
		for article in articles:
			item = ArticleItem()
			item['type'] = "article"
			item['postId'] = self.name+str(article['id'])

			item['title'] = article['headline']
			item['url'] = article['linkUrl']

			if 'images' in article and article['images']:
				item['image'] = article["images"][0]["URL"]
			elif 'thumbnail' in article:
				item['image'] = article["thumbnail"]["URL"]
			else:
				continue

			item['date'] = article['date']
			item['src'] = 'espnfc'
			item['lang'] = 'en'
			if 'summary' in article.keys():
				item['summary'] = article["summary"]
			tags = []
			for tag in article["contentCategory"]:
				tags.append(tag['name'])

			item['tags'] = tags

			tree = etree.HTML(article['body'])
			content = tree.xpath(".//p/text()")
			item['content'] = ' '.join(content)
			item['itemIndex'] = self.itemCount
			self.itemCount = self.itemCount+1
			item['account_image'] = ' '
			yield item