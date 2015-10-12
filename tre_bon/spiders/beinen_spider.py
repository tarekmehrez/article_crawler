# Author: Tarek

import scrapy
import re

from datetime import datetime
from tre_bon.items import ArticleItem
from scrapy.exceptions import CloseSpider


class BeinENpider(scrapy.Spider):


	name = 'bein_en'
	start_urls=["http://www.beinsports.com/en/football/news/" + str(i+1) for i in range(5)]


	def parse(self,response):

		for sel in response.xpath(".//li[contains(@class,'content-gallery__item w50')]"):
			item = ArticleItem()
			item['type'] = "article"

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
		item['summary'] = ' '
		item['tags'] = ' '
		yield item
