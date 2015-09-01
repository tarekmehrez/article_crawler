import scrapy
import json
import urllib2

from tre_bon.items import ESPNItem
from scrapy.http import HtmlResponse

# TODO: handle endoding and format in tags, summary and titles
# TODO: make sure all tags have similar formats (same tags are grouped)
# TODO: handle date format


class ESPNSpider(scrapy.Spider):
	name = 'espn'
	allowed_domains = ["espnfc.com"]
	start_urls=["http://www.espnfc.com/news"]

	def parse(self, response):


		data = json.load(urllib2.urlopen("http://www.espnfc.com/api/feed?xhr=1&t=54&device=pc&limit=100&content=story&offset=0&key=espnfc-en-www-index-news-600"))
		articles = data['data']['features']


		for article in articles:
			item = ESPNItem()
			item['title'] = article['headline']
			item['url'] = article['linkUrl']

			if article["images"]:
				item['image'] = article["images"][0]["imageLocation"]
			else:
				item['image'] = article["thumbnail"]["URL"]

			item['datetime'] = article["source"]["createDate"]
			item['src'] = 'espnfc'
			item['lang'] = 'en'
			item['summary'] = article["summary"]
			tags = []
			for tag in article["contentCategory"]:
				tags.append(tag['name'])

			item['tags'] = tags

			yield item