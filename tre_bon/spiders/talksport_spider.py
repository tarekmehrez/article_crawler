# Author: Tarek

import scrapy

from tre_bon.items import ArticleItem
import re

class TalkSportpider(scrapy.Spider):
	name = 'talksport'
	allowed_domains = ["talksport.com"]
	start_urls=["http://talksport.com/football?page=" + str(i) for i in range(10)]

	itemCount = 1
	def parse(self,response):
		for sel in response.xpath(".//div[contains(@class,'node node-article node-teaser clearfix')]"):
			item = ArticleItem()
			item['type'] = "article"

			relative_url = sel.xpath(".//a/@href")[0].extract()
			url = response.urljoin(relative_url)

			item['url'] = url
			item['title'] = sel.xpath(".//h2/a/text()")[0].extract()
			item['summary'] = sel.xpath(".//div[contains(@class,'field field-name-field-intro field-type-text-long field-label-hidden')]/div/div/text()")[0].extract()
			item['src'] = 'talksport'
			item['lang'] = 'en'
			item['itemIndex'] = self.itemCount
			self.itemCount = self.itemCount+1
			yield scrapy.Request(url, callback=self.parse_article,meta={'item': item})

	def parse_article(self, response):
		item = response.meta['item']

		item['image'] = response.xpath(".//div[contains(@class,'field-item even')]/img/@src")[0].extract()
		item['tags'] = response.xpath(".//ul[contains(@class,'links')]/li/a/text()").extract()
		item['date'] = response.xpath(".//div[contains(@class,'meta submitted')]/text()")[2].extract().replace('|','').strip()
		content =  response.xpath(".//div[contains(@class,'field-item even')]/p/text()").extract()
		item['content'] = ' '.join(content)
		item['account_image'] = ' '
		postId  = re.match(r'.*/(.*)', response.url, re.M|re.I)
		if postId:
			item['postId'] =postId.group(1)+ self.name
		else:
			item['postId'] = item['title']
		yield item