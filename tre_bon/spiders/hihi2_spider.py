import scrapy

from tre_bon.items import ArticleItem


class Hihi2Spider(scrapy.Spider):
	name = 'hihi2'
	allowed_domains = ["hihi2.com"]
	start_urls=["http://hihi2.com/category/football-news/page/" + str(i+1) for i in range(5)]


	def parse(self,response):

		for sel in response.xpath(".//div[contains(@id,'content-loop')]/div[starts-with(@id,'post-')]"):
			item = ArticleItem()
			item['type'] = "article"

			url = sel.xpath(".//h2/a/@href")[0].extract()

			item['url'] = url
			item['title'] =  sel.xpath(".//h2/a/text()")[0].extract()
			item['summary'] = sel.xpath(".//div[contains(@class,'entry-excerpt')]/text()")[0].extract()
			item['src'] = 'hihi2'
			item['lang'] = 'ar'
			item['date'] = sel.xpath(".//span[contains(@class,'entry-date')]/text()")[0].extract().replace('[','').replace(']','')
			yield scrapy.Request(url, callback=self.parse_article,meta={'item': item})

	def parse_article(self, response):
		item = response.meta['item']
		item['image'] = response.xpath(".//div[contains(@class,'entry-content')]/p/a/@href")[0].extract()
		item['tags'] = response.xpath(".//div[contains(@class,'entry-tags')]/a/text()").extract()
		content = response.xpath(".//div[contains(@class,'entry-content')]/p/text()").extract()
		item['content'] = ' '.join(content)
		yield item
