import scrapy

from tre_bon.items import TreBonItem


# TODO: handle date format
# TODO: handle endoding and format in tags, summary and titles
# TODO: make sure all tags have similar formats (same tags are grouped)


class Hihi2Spider(scrapy.Spider):
	name = 'hihi2'
	allowed_domains = ["hihi2.com"]
	start_urls=["http://hihi2.com/category/football-news",
				"http://hihi2.com/category/football-news/page/2",
				"http://hihi2.com/category/football-news/page/3",
				"http://hihi2.com/category/football-news/page/4",
				"http://hihi2.com/category/football-news/page/5",
				"http://hihi2.com/category/football-news/page/6",
				"http://hihi2.com/category/football-news/page/7",
				"http://hihi2.com/category/football-news/page/8",
				"http://hihi2.com/category/football-news/page/9",
				"http://hihi2.com/category/football-news/page/10",]


	def parse(self,response):

		for sel in response.xpath(".//div[contains(@id,'content-loop')]/div[starts-with(@id,'post-')]"):
			item = TreBonItem()

			url = sel.xpath(".//h2/a/@href")[0].extract()

			item['url'] = url
			item['title'] =  sel.xpath(".//h2/a/text()")[0].extract()
			item['summary'] = sel.xpath(".//div[contains(@class,'entry-excerpt')]/text()")[0].extract()
			item['src'] = 'hihi2'
			item['lang'] = 'ar'
			item['datetime'] = sel.xpath(".//span[contains(@class,'entry-date')]/text()")[0].extract().replace('[','').replace(']','').strip()
			yield scrapy.Request(url, callback=self.parse_article,meta={'item': item})

	def parse_article(self, response):
		item = response.meta['item']
		item['image'] = response.xpath(".//div[contains(@class,'entry-content')]/p/a/@href")[0].extract()

		item['tags'] = response.xpath(".//div[contains(@class,'entry-tags')]/a/text()").extract()
		yield item
