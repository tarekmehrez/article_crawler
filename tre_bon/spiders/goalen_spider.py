import scrapy
import re
import urllib
import urlparse

from tre_bon.items import GoalENItem
from scrapy.http import HtmlResponse

# TODO: handle endoding and format in tags, summary and titles
# TODO: make sure all tags have similar formats (same tags are grouped)
# TODO: handle date format


class GoalENSpider(scrapy.Spider):
	name = 'goal_en'
	# allowed_domains = ["goal.com/en"]
	start_urls=["http://www.goal.com/en/news/archive/1",
				"http://www.goal.com/en/news/archive/2",
				"http://www.goal.com/en/news/archive/3",
				"http://www.goal.com/en/news/archive/4",
				"http://www.goal.com/en/news/archive/5",
				"http://www.goal.com/en/news/archive/6",
				"http://www.goal.com/en/news/archive/7",
				"http://www.goal.com/en/news/archive/8",
				"http://www.goal.com/en/news/archive/9",
				"http://www.goal.com/en/news/archive/10"]

	def parse(self,response):
		for sel in response.xpath("//div[contains(@id,'news-archive')]//ul/li"):
			item = GoalENItem()
			article_info = sel.xpath(".//div[contains(@class,'articleInfo')]")[0]

			item['title'] = article_info.xpath(".//a/text()")[0].extract()
			if sel.xpath(".//div[contains(@class,'articleSummary')]/text()"):
				item['summary'] = sel.xpath(".//div[contains(@class,'articleSummary')]/text()")[0].extract()
			item['datetime'] = str(sel.xpath("../../div[contains(@class,'date')]/text()")[0].extract()) + str(sel.xpath(".//span")[1].xpath(".//text()")[0].extract())

			relative_url = str(article_info.xpath(".//a/@href")[0].extract())
			url = response.urljoin(relative_url).replace("/en/news/archive","")
			item['url'] = url

			item['src'] = 'goal_en'
			item['lang'] = 'en'

			tag = str(sel.xpath(".//strong/text()")[0].extract().encode("utf-8"))
			tag = re.sub(r'[^\x00-\x7F]+',' ', tag).replace('-','').strip().lower().replace(' ','_')
			item['tags'] = [tag]

			yield scrapy.Request(url, callback=self.parse_article,meta={'item': item})

	def parse_article(self, response):
		item = response.meta['item']

		if not response.xpath(".//img[contains(@class,'article-image')]/@src"):
			yield item
		else:
			item['image'] = response.xpath(".//img[contains(@class,'article-image')]/@src")[0].extract()
			self.logger.debug('in parse article')
			for sel in response.xpath(".//li[contains(@class,'tags')]/a/text()"):
				tag = str(sel.extract().encode('utf-8'))
				tag = re.sub(r'[^\x00-\x7F]+',' ', tag).replace('-','').strip().lower().replace(' ','_')

				item['tags'].append(tag)

			yield item