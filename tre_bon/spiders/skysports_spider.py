import scrapy

from tre_bon.items import TreBonItem

# TODO: handle date format
# TODO: handle endoding and format in tags, summary and titles
# TODO: make sure all tags have similar formats (same tags are grouped)


class SkySportsSpider(scrapy.Spider):
	name = 'skysports'
	allowed_domains = ["skysports.com"]
	start_urls=["http://www.skysports.com/football/news",
				"http://www.skysports.com/football/news/more/2",
				"http://www.skysports.com/football/news/more/3",
				"http://www.skysports.com/football/news/more/4",
				"http://www.skysports.com/football/news/more/5",
				"http://www.skysports.com/football/news/more/6",
				"http://www.skysports.com/football/news/more/7",
				"http://www.skysports.com/football/news/more/8",
				"http://www.skysports.com/football/news/more/9",
				"http://www.skysports.com/football/news/more/10"]


	def parse(self,response):

		for sel in response.xpath(".//div[contains(@class,'news-list__item news-list__item--show-thumb-bp30')]"):
			item = TreBonItem()

			url = sel.xpath(".//h4/a/@href")[0].extract()

			item['url'] = url
			item['title'] = sel.xpath(".//h4/a/text()")[0].extract().strip()
			item['summary'] = sel.xpath(".//p[contains(@class,'news-list__snippet')]/text()")[0].extract()
			item['src'] = 'skysports'
			item['lang'] = 'en'
			item['datetime'] =  sel.xpath(".//span[contains(@class,'label__timestamp')]/text()")[0].extract()
			yield scrapy.Request(url, callback=self.parse_article,meta={'item': item})

	def parse_article(self, response):
		item = response.meta['item']
		if response.xpath(".//figure/div/div/img/@data-src"):
			item['image'] = response.xpath(".//figure/div/div/img/@data-src")[0].extract()
		elif response.xpath(".//figure/div/div/div/img/@data-src"):
			item['image'] = response.xpath(".//figure/div/div/div/img/@data-src")[0].extract()
		else:
			return
		yield item