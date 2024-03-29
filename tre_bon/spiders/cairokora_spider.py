# Author: Tarek

import scrapy

from tre_bon.items import ArticleItem
import re

class CairoKoraSpider(scrapy.Spider):
	name = 'cairokora'
	allowed_domains = ["cairokora.com","cairokora.youm7.com","kora.youm7.com"]
	start_urls=		["http://www.cairokora.com/category/%D9%83%D8%B1%D8%A9-%D9%85%D8%B5%D8%B1%D9%8A%D8%A9/page/" + str(i+1) for i in range(10)] \
				+	["http://www.cairokora.com/category/%D8%AD%D9%88%D9%84-%D8%A7%D9%84%D8%B9%D8%A7%D9%84%D9%85/page/" + str(i+1) for i in range(10)]
	itemCount = 1
	def parse(self,response):
		
		for sel in response.xpath(".//div[contains(@class,'slider_bottom clearfix')]/div[starts-with(@class,'section')]"):
			item = ArticleItem()
			item['type'] = "article"

			url = sel.xpath(".//a[contains(@class,'title')]/@href")[0].extract()
			item['url'] = url
			item['title'] = sel.xpath(".//a[contains(@class,'title')]/h3/text()")[0].extract()
			item['summary'] = sel.xpath(".//p[contains(@class,'desc')]/text()")[0].extract()
			item['src'] = 'cairokora'
			item['lang'] = 'ar'
			item['itemIndex'] = self.itemCount
			itemCount = self.itemCount+1
			yield scrapy.Request(url, callback=self.parse_article,meta={'item': item})

		for sel in response.xpath(".//div[contains(@class,'thum clearfix')]"):
			url = sel.xpath(".//a[contains(@class,'title')]/@href")[0].extract()
			item['url'] = url
			item['title'] = sel.xpath(".//a[contains(@class,'title')]/h3/text()")[0].extract()
			item['src'] = 'cairokora'
			item['lang'] = 'ar'
			item['itemIndex'] = self.itemCount
			self.itemCount = self.itemCount+1
			yield scrapy.Request(url, callback=self.parse_article,meta={'item': item})

	def parse_article(self, response):
		item = response.meta['item']
		postId  = re.match(r'.*/([0-9]*/.*)', response.url, re.M|re.I)
		if postId:
			item['postId'] = self.name+postId.group(1)
		else:
			item['postID'] = item['url']
		item['date'] =  response.xpath(".//p[contains(@class,'writer')]/text()")[0].extract()
		item['image'] = response.xpath(".//div[contains(@class,'article_img')]/img/@src")[0].extract()
		item['tags'] = response.xpath(".//div[contains(@class,'tags clearfix')]/ul/a/li/text()").extract()

		content = response.xpath(".//div[contains(@class,'article_text')]/p/text()").extract()
		item['content'] = ' '.join(content)
		item['account_image'] = ' '
		yield item
