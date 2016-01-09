# Author: Tarek

import scrapy

from tre_bon.items import ArticleItem
from bs4 import BeautifulSoup

import re


class TeamTalkSpider(scrapy.Spider):
	name = 'teamtalk'
	allowed_domains = ["teamtalk.com"]
	start_urls = ["http://www.teamtalk.com/all-the-news/page/" + str(i+1) for i in range(10)]

	itemCount = 1

	def parse(self,response):


		# getting features articles
		if len(str(response).replace('<','').replace('>','').split('/')) < 5:

			item = ArticleItem()
			item['type'] = "article"

			url = response.xpath(".//section[@class='hero']/div/figure/a/@href")[0].extract()
			item['url']= url
			item['title']= BeautifulSoup(response.xpath(".//section[@class='hero']/div/figure/a/figcaption/h2")[0].extract(),"lxml").string
			item['src']='teamtalk'
			item['lang']='en'
			yield scrapy.Request(url, callback=self.parse_article,meta={'item': item})

			for sel in response.xpath(".//ul[@class='hero__list']/li"):
				item = ArticleItem()
				item['type'] = "article"
				url = sel.xpath(".//a/@href")[0].extract()
				item['url'] =  url
				item['src']='teamtalk'
				item['lang']='en'
				item['title']= BeautifulSoup(sel.xpath(".//h3")[0].extract(),"lxml").string
				yield scrapy.Request(url, callback=self.parse_article,meta={'item': item})


		# getting normal articles

		for sel in response.xpath(".//ul[@class='articleList__list']/li"):
			item = ArticleItem()
			item['type'] = "article"
			url = sel.xpath(".//a/@href")[0].extract()
			item['url'] = url
			item['title'] = BeautifulSoup(sel.xpath(".//h3")[0].extract(),"lxml").string


			item['summary'] = BeautifulSoup(sel.xpath(".//p")[0].extract(),"lxml").string
			item['src'] = 'teamtalk'
			item['lang'] = 'en'
			item['itemIndex'] = self.itemCount
			self.itemCount += 1
			yield scrapy.Request(url, callback=self.parse_article,meta={'item': item})


	def parse_article(self, response):
		item = response.meta['item']

		item['date'] = BeautifulSoup(response.xpath(".//header/div/p")[0].extract(),"lxml").string.split(':',1)[1].strip().split(" ",1)[1]
		if response.xpath(".//span[@class='article__imgWrapper']/img/@data-src"):
			item['image'] = response.xpath(".//span[@class='article__imgWrapper']/img/@data-src")[0].extract()
		else:
			item['image'] = response.xpath(".//span[@class='article__imgWrapper']/img/@src")[0].extract()
		content = response.xpath(".//section[@class='article__body']/p").extract()
		item['content']= ''
		for sen in content:
			cleaned = BeautifulSoup(str(sen.encode("utf-8")),"lxml").string
			if cleaned:
				item['content'] += cleaned
		item['tags'] = ' '
		item['account_image'] = ' '
		postId  = re.match(r'.*/([0-9]*)', response.url, re.M|re.I)
		if postId:
			item['postId'] = self.name+postId.group(1)
		else:
			item['postId'] = item['title']
		print item
		yield item
