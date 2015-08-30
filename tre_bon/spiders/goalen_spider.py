import scrapy
import re
from tre_bon.items import GoalENItem
from scrapy.http import Request


class GoalENSpider(scrapy.Spider):
	name = 'goalen'
	allowed_domains = ["goal.com/en"]
	start_urls=["http://www.goal.com/en/news/archive/1"]


	def parse(self,response):


		for sel in response.xpath("//div[contains(@id,'news-archive')]//ul/li"):
			item = GoalENItem()
			item['image'] = str(sel.xpath(".//img/@src")[0].extract()).replace("_thumb","")
			article_info = sel.xpath(".//div[contains(@class,'articleInfo')]")[0]

			url = "http://www.goal.com" + str(article_info.xpath(".//a/@href")[0].extract())
			item['url'] = url
			item['title'] = article_info.xpath(".//a/text()")[0].extract()

			item['summary'] = sel.xpath(".//div[contains(@class,'articleSummary')]/text()")[0].extract()
			item['date'] = sel.xpath("../../div[contains(@class,'date')]/text()")[0].extract()
			item['time'] = sel.xpath(".//span")[1].xpath(".//text()")[0].extract()

			item['tags'] = []
			tag = str(sel.xpath(".//strong/text()")[0].extract().encode("utf-8"))
			tag = re.sub(r'[^\x00-\x7F]+',' ', tag).replace('-','').strip().lower().replace(' ','_')
			item['tags'].append(tag)

			self.logger.warning('here in response')

			yield item
			# request = scrapy.Request("https://www.google.com.eg/",callback=self.parse_tags)
			# request.meta['item'] = item
			# yield request

	def parse_tags(self, response):
		self.logger.warning('here in tags')

		item = response.meta['item']
		tags = []
		for sel in response.xpath(".//li[contains(@class,'tags')]/a/text()"):
			tag = str(sel.extract().encode('utf-8'))
			tag = re.sub(r'[^\x00-\x7F]+',' ', tag).strip().lower().replace(' ','_')

			tags.append(tag)

		item['tags'] = tags
		return item

# def parse_page1(self, response):
#     item = MyItem()
#     item['main_url'] = response.url
#     request = scrapy.Request("http://www.example.com/some_page.html",
#                              callback=self.parse_page2)
#     request.meta['item'] = item
#     return request

# def parse_page2(self, response):
#     item = response.meta['item']
#     item['other_url'] = response.url
#     return item