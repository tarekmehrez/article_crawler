# Author: Tarek

import scrapy

from tre_bon.items import ArticleItem
import re



class SkySportsSpider(scrapy.Spider):
	name = 'skysports'
	allowed_domains = ["skysports.com"]
	start_urls=["http://www.skysports.com/football/news/more/" + str(i+1) for i in range(5)]

	itemCount = 1
	def parse(self,response):
		itemCount = 1
		for sel in response.xpath(".//div[contains(@class,'news-list__item news-list__item--show-thumb-bp30')]"):
			item = ArticleItem()
			item['type'] = "article"

			url = sel.xpath(".//h4/a/@href")[0].extract()

			item['url'] = url
			item['title'] = sel.xpath(".//h4/a/text()")[0].extract()
			if sel.xpath(".//p[contains(@class,'news-list__snippet')]/text()"): item['summary'] = sel.xpath(".//p[contains(@class,'news-list__snippet')]/text()")[0].extract()
			item['src'] = 'SkySports'
			item['lang'] = 'en'
			item['date'] =  sel.xpath(".//span[contains(@class,'label__timestamp')]/text()")[0].extract()
			item['itemIndex'] = self.itemCount
			self.itemCount = self.itemCount+1
			yield scrapy.Request(url, callback=self.parse_article,meta={'item': item})

	def parse_article(self, response):
		item = response.meta['item']
		if response.xpath(".//figure/div/div/img/@data-src"):
			item['image'] = response.xpath(".//figure/div/div/img/@data-src")[0].extract()
		elif response.xpath(".//figure/div/div/div/img/@data-src"):
			item['image'] = response.xpath(".//figure/div/div/div/img/@data-src")[0].extract()
		else:
			return

		if response.xpath(".//div[contains(@class,'article__body article__body--lead')]/p/text()").extract():
			content = response.xpath(".//div[contains(@class,'article__body article__body--lead')]/p/text()").extract()
			item['content'] = ' '.join(content)
			# item['tags'] = ','.join(content)
		item['account_image'] = ' '
		postId  = re.match(r'.*/([0-9]*)/([0-9]*)/.*', response.url, re.M|re.I)
		if postId:
			item['postId'] = self.name+postId.group(1)+postId.group(2)
		else:
			item['postId'] = item['title']
		yield item
