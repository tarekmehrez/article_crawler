# Author: Tarek

import scrapy

from tre_bon.items import ArticleItem

import re


class WhoScoredSpider(scrapy.Spider):
	name = 'whoscored'
	allowed_domains = ["whoscored.com"]
	start_urls = ["http://www.whoscored.com/Editorial?page=" + str(i+1) for i in range(10)]

	itemCount = 1

	def parse(self,response):

		for sel in response.xpath(".//ul[@class='ws-editorial-list-items']/a"):
			item = ArticleItem()
			relative_url =  sel.xpath(".//@href")[0].extract()
			url = response.urljoin(relative_url)
			item['url'] = url
			item['title']= sel.xpath(".//div[@class='ws-editorial-title']/text()")[0].extract().strip()
			item['src']='whoscored'
			item['lang']='en'
			item['type']='article'
			item['summary']=''
			yield scrapy.Request(url, callback=self.parse_article,meta={'item': item})


	def parse_article(self, response):
		item = response.meta['item']
		item['image']= response.xpath(".//span[@class='post-text']/p/img/@src")[0].extract()
		item['date'] = response.xpath(".//span[@class='post-date']/text()")[0].extract().split(" ",1)[1].split(',',1)[1].strip()

		content =  response.xpath(".//span[@class='post-text']/p/span/text()").extract()
		item['content'] = ' '.join(content)

		item['tags'] = response.xpath(".//div[@class='post-tags']/a/text()").extract()
		item['account_image'] = ' '
		postId  = re.match(r'.*/([0-9]*)', response.url, re.M|re.I)
		if postId:
			item['postId'] = self.name+postId.group(1)
		else:
			item['postId'] = item['title']
		print item
		yield item
