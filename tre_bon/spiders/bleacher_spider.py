# Author: Tarek

import scrapy
import json
import urllib2

from tre_bon.items import ArticleItem


class BleacherSpider(scrapy.Spider):
	name = 'bleacher'
	allowed_domains = ["bleacherreport.com"]
	start_urls=["http://bleacherreport.com/world-football"]
	itemCount = 1
	def parse(self, response):


		data = json.load(urllib2.urlopen("http://layser.bleacherreport.com/api/team_stream/world-football?tags=null&limit=100"))
		articles = data['streams'][0]['items']
		for article in articles:
			item = ArticleItem()
			item['postId'] = self.name+article["id"]
			item['type'] = "article"

			item['title'] = article['title']

			url = article['permalink']

			item['url'] = article['permalink']

			item['image'] = article["primary_image_650x440"]


			item['date'] = article["publishedAt"]
			item['src'] = 'bleacher_report'
			item['lang'] = 'en'
			item['tags'] = article['tags']
			item['itemIndex'] = self.itemCount
			self.itemCount = self.itemCount+1
			yield scrapy.Request(url, callback=self.parse_article,meta={'item': item})


	def parse_article(self,response):
		item = response.meta['item']
		content = response.xpath(".//div[contains(@class,'article_body cf')]/p/text()").extract()
		item['content'] = ' '.join(content)
		item['summary'] = ' '.join(response.xpath('/html/head/meta[@name="description"]/@content').extract())
		item['account_image'] = ' '
		yield item