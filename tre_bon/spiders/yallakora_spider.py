# Author: Tarek

import scrapy

from tre_bon.items import ArticleItem
import re


class YallaKoraSpider(scrapy.Spider):
	name = 'yallakora'
	allowed_domains = ["yallakora.com"]
	start_urls= 	["http://www.yallakora.com/News/LoadMoreCategory.aspx?page=" + str(i+1) + "&newsregion=1&type=26" 	for i in range(5)] \
				+ 	["http://www.yallakora.com/News/LoadMoreCategory.aspx?page=" + str(i+1) + "&newsregion=1&type=1" 	for i in range(5)]

	itemCount = 1
	def parse(self,response):
		for sel in response.xpath(".//li[contains(@class,'ClipItem')]"):
			item = ArticleItem()
			item['type'] = "article"

			relative_url = sel.xpath(".//a[contains(@class,'NewsTitle')]/@href")[0].extract()
			url = response.urljoin(relative_url)
			item['summary'] = sel.xpath(".//a[contains(@class,'NewsTitle')]/text()")[0].extract()
			item['url'] = url
			item['title'] = sel.xpath(".//a[contains(@class,'NewsTitle')]/text()")[0].extract().strip()
			item['src'] = 'yallakora'
			item['lang'] = 'ar'
			item['itemIndex'] = self.itemCount
			itemCount = self.itemCount+1
			yield scrapy.Request(url, callback=self.parse_article,meta={'item': item})

	def parse_article(self, response):
		item = response.meta['item']

		item['image'] = response.xpath(".//div[contains(@class,'ArticleIMG')]/img/@src")[0].extract()
		if response.xpath(".//span[contains(@class,'PortfolioDate')]/text()"):
			item['date'] = response.xpath(".//span[contains(@class,'PortfolioDate')]/text()")[0].extract()
		item['tags'] = ','.join(response.xpath(".//ul[contains(@class,'TourTabs floatRight')]/li/a/span/text()").extract())
		content=   response.xpath(".//div[contains(@class,'articleBody')]/text()").extract()
		item['content'] = ' '.join(content)
		item['account_image'] = ' '
		postId  = re.match(r'.*/([0-9]*)/([0-9]*)/.*', response.url, re.M|re.I)
		if postId:
			item['postId'] =postId.group(1)+postId.group(2)+ self.name
		else:
			item['postId'] = item['title']
		yield item
