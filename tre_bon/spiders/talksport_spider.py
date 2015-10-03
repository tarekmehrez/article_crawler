# Author: Tarek

import scrapy

from tre_bon.items import ArticleItem

class TalkSportpider(scrapy.Spider):
	name = 'talksport'
	allowed_domains = ["talksport.com"]
	start_urls=["http://talksport.com/football?page=" + str(i+1) for i in range(5)]


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
			yield scrapy.Request(url, callback=self.parse_article,meta={'item': item})

	def parse_article(self, response):
		item = response.meta['item']

		item['image'] = response.xpath(".//div[contains(@class,'field-item even')]/img/@src")[0].extract()
		item['tags'] = response.xpath(".//ul[contains(@class,'links')]/li/a/text()").extract()
		item['date'] = response.xpath(".//div[contains(@class,'meta submitted')]/text()")[2].extract().replace('|','').strip()
		content =  response.xpath(".//div[contains(@class,'field-item even')]/p/text()").extract()
		item['content'] = ' '.join(content)
		yield item