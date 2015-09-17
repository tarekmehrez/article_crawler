import scrapy
import re

from datetime import datetime
from tre_bon.items import TreBonItem
from scrapy.exceptions import CloseSpider

# TODO: handle date format
# TODO: handle endoding and format in tags, summary and titles
# TODO: make sure all tags have similar formats (same tags are grouped)




class BeinENpider(scrapy.Spider):


	name = 'bein_en'
	start_urls=["http://www.beinsports.com/en/football/news/" + str(i+1) for i in range(2)]


	def parse(self,response):

		for sel in response.xpath(".//li[contains(@class,'content-gallery__item w50')]"):
			item = TreBonItem()

			item['date'] = sel.xpath(".//time/@datetime")[0].extract()


			relative_url = sel.xpath(".//figcaption/a/@href")[0].extract()
			url = response.urljoin(relative_url)
			item['url'] = url
			item['title'] = sel.xpath(".//figcaption/a/text()")[0].extract()

			item['src'] = 'bein'
			item['lang'] = 'en'
			yield scrapy.Request(url, callback=self.parse_article,meta={'item': item})

	def parse_article(self, response):
		item = response.meta['item']
		item['image'] = response.xpath(".//div[contains(@class,'visuel-article_hero')]/img/@src")[0].extract()
		content = response.xpath(".//main/p/text()").extract()
		item['content'] = ' '.join(content)
		yield item
