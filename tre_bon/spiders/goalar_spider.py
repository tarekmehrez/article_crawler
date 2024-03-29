# Author: Tarek

import scrapy
import re


from tre_bon.items import ArticleItem

class GoalARSpider(scrapy.Spider):
	name = 'goal_ar'
	# allowed_domains = ["goal.com/en"]
	start_urls=["http://www.goal.com/ar/news/archive/" + str(i+1) for i in range(5)]
	itemCount = 1
	def parse(self,response):
		for sel in response.xpath("//div[contains(@id,'news-archive')]//ul/li"):
			item = ArticleItem()
			item['type'] = "article"

			article_info = sel.xpath(".//div[contains(@class,'articleInfo')]")[0]

			item['title'] = article_info.xpath(".//a/text()")[0].extract()
			if sel.xpath(".//div[contains(@class,'articleSummary')]/text()"):
				item['summary'] = sel.xpath(".//div[contains(@class,'articleSummary')]/text()")[0].extract()
			item['date'] = str(sel.xpath("../../div[contains(@class,'date')]/text()")[0].extract().encode('utf8')) + str(sel.xpath(".//span")[1].xpath(".//text()")[0].extract().encode('utf8'))

			relative_url = str(article_info.xpath(".//a/@href")[0].extract())
			url = response.urljoin(relative_url).replace("/en/news/archive","")
			item['url'] = url

			item['src'] = 'goal'
			item['lang'] = 'ar'

			tag = sel.xpath(".//strong/text()")[0].extract()

			item['tags'] = [tag]
			item['itemIndex'] = self.itemCount
			self.itemCount = self.itemCount+1
			yield scrapy.Request(url, callback=self.parse_article,meta={'item': item})

	def parse_article(self, response):
		item = response.meta['item']
		item['image'] = ''
		if response.xpath(".//img[contains(@class,'article-image')]/@src"):
			item['image'] = response.xpath(".//img[contains(@class,'article-image')]/@src")[0].extract()

		item['tags'] = ','.join(response.xpath(".//li[contains(@class,'tags')]/a/text()").extract())
		content = 		response.xpath(".//div[contains(@class,'article-text')]/p/text()").extract() \
					+ 	response.xpath(".//div[contains(@class,'article-text')]/text()").extract() \
					+	response.xpath(".//div[@class='article-text']/p/span/text()").extract()
		item['content'] = ' '.join(content)
		item['account_image'] = ' '
		postId  = re.match(r'.*/([0-9]*)/.*', response.url, re.M|re.I)
		if postId:
			item['postId'] = self.name+postId.group(1)
		else:
			item['postId'] = item['title']
		yield item

