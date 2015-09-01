import scrapy
import json
import urllib2

from tre_bon.items import ESPNItem
from scrapy.http import HtmlResponse

class GoalENSpider(scrapy.Spider):
	name = 'espn'
	allowed_domains = ["espnfc.com"]
	start_urls=["http://www.espnfc.com/news"]

	def parse(self, response):

		item = ESPNItem()

		data = json.load(urllib2.urlopen("http://www.espnfc.com/api/feed?xhr=1&t=54&device=pc&limit=100&content=story&offset=0&key=espnfc-en-www-index-news-600"))
		articles = data['data']['features']
		self.logger.debug(len(articles))


		for article in articles:
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

		# filename = response.url.split("/")[-2] + '.html'
		# with open(filename, 'wb') as f:
		# 	f.write(response.body)

		# for sel in response.xpath(".//article"):
		# 	item = ESPNItem()

		# 	item['url'] = sel.xpath(".//h1/a/@href")[0].extract()
		# 	item['title'] = sel.xpath(".//h1/a/text()")[0].extract()
		# 	item['datetime'] = sel.xpath(".//time/@datetime")[0].extract()
		# 	item['image'] = sel.xpath(".//img/@src")[0].extract()
		# 	item['src'] = 'espnfc'
		# 	item['lang'] = 'en'

		# 	item['tags'] = sel.xpath(".//ul[contains(@class,'tags')]/li/a/text()").extract()

		# 	yield item