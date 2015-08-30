import scrapy
import re
import urllib


from tre_bon.items import ESPNItem
from scrapy.http import HtmlResponse

class GoalENSpider(scrapy.Spider):
	name = 'espn'
	allowed_domains = ["espnfc.com"]
	start_urls=["http://www.espnfc.com/news"]

	def parse(self, response):
		for sel in response.xpath(".//article"):
			item = ESPNItem()

			item['url'] = sel.xpath(".//h1/a/@href")[0].extract()
			item['title'] = sel.xpath(".//h1/a/text()")[0].extract()
			item['datetime'] = sel.xpath(".//time/@datetime")[0].extract()
			item['image'] = sel.xpath(".//img/@src")[0].extract()
			item['src'] = 'espnfc'
			item['lang'] = 'en'

			item['tags'] = sel.xpath(".//ul[contains(@class,'tags')]/li/a/text()").extract()

			yield item