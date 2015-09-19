import scrapy

from tre_bon.items import ArticleItem

class CairoKoraSpider(scrapy.Spider):
	name = 'cairokora'
	allowed_domains = ["cairokora.com"]
	start_urls=		["http://www.cairokora.com/category/%D9%83%D8%B1%D8%A9-%D9%85%D8%B5%D8%B1%D9%8A%D8%A9/page/" + str(i+1) for i in range(10)] \
				+	["http://www.cairokora.com/category/%D8%AD%D9%88%D9%84-%D8%A7%D9%84%D8%B9%D8%A7%D9%84%D9%85/page/" + str(i+1) for i in range(10)]

	def parse(self,response):

		for sel in response.xpath(".//div[contains(@class,'slider_bottom clearfix')]/div[starts-with(@class,'section')]"):
			item = ArticleItem()
			item['type'] = "article"

			url = sel.xpath(".//a[contains(@class,'title')]/@href")[0].extract()
			item['url'] = url
			item['title'] = sel.xpath(".//a[contains(@class,'title')]/h3/text()")[0].extract()
			item['summary'] = sel.xpath(".//p[contains(@class,'desc')]/text()")[0].extract()
			item['src'] = 'cairokora'
			item['lang'] = 'ar'
			yield scrapy.Request(url, callback=self.parse_article,meta={'item': item})

		for sel in response.xpath(".//div[contains(@class,'thum clearfix')]"):
			url = sel.xpath(".//a[contains(@class,'title')]/@href")[0].extract()
			item['url'] = url
			item['title'] = sel.xpath(".//a[contains(@class,'title')]/h3/text()")[0].extract()
			item['src'] = 'cairokora'
			item['lang'] = 'ar'
			yield scrapy.Request(url, callback=self.parse_article,meta={'item': item})

	def parse_article(self, response):
		item = response.meta['item']
		item['date'] =  response.xpath(".//p[contains(@class,'writer')]/text()")[0].extract()
		item['image'] = response.xpath(".//div[contains(@class,'article_img')]/img/@src")[0].extract()
		item['tags'] = response.xpath(".//div[contains(@class,'tags clearfix')]/ul/a/li/text()").extract()

		content = response.xpath(".//div[contains(@class,'article_text')]/p/text()").extract()
		item['content'] = ' '.join(content)


		yield item
