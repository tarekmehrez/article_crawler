# Author: Tarek

import scrapy

from tre_bon.items import ArticleItem
import re


class KorabiaSpider(scrapy.Spider):
	name = 'korabia'
	allowed_domains = ["korabia.com"]
	start_urls = ["http://www.korabia.com/News?page=" + str(i+1) for i in range(10)]

	itemCount = 1
	def parse(self,response):
		for sel in response.xpath(".//ul[contains(@class,'all-news-list')]/li"):
			item = ArticleItem()
			item['type'] = "article"

			relative_url = sel.xpath(".//div/h5/a/@href")[0].extract()
			url = response.urljoin(relative_url)
			item['url'] = url
			item['title'] = sel.xpath(".//div/h5/a/text()")[0].extract()


			item['summary'] = sel.xpath(".//div/p/text()")[0].extract()
			item['src'] = 'korabia'
			item['lang'] = 'ar'
			item['date'] = sel.xpath(".//div/p[contains(@class,'info')]/span/text()")[0].extract()
			item['itemIndex'] = self.itemCount
			self.itemCount = self.itemCount+1
			yield scrapy.Request(url, callback=self.parse_article,meta={'item': item})


	def parse_article(self, response):
		item = response.meta['item']
		item['image'] = response.xpath(".//div[@class='img infographic']/img/@src")[0].extract()

		content = response.xpath(".//p[contains(@class,'main-type-text')]/text()").extract()
		item['content'] = ' '.join(content)
		item['tags'] = ' '
		item['account_image'] = ' '
		postId  = re.match(r'.*/([0-9]+[a-zA-Z0-9]*)/', response.url, re.M|re.I)
		if postId:
			item['postId'] = self.name+postId.group(1)
		else:
			item['postId'] = item['title']

		yield item
