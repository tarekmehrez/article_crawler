import scrapy

from tre_bon.items import TreBonItem

# TODO: add DOWNLOADER_MIDDLEWARES to bypass blocked requests
# TODO: handle endoding and format in tags, summary and titles
# TODO: make sure all tags have similar formats (same tags are grouped)
# TODO: handle date format

class TalkSportpider(scrapy.Spider):
	name = 'talksport'
	allowed_domains = ["talksport.com"]
	start_urls=["http://talksport.com/football",
				"http://talksport.com/football?page=1",
				"http://talksport.com/football?page=2",
				"http://talksport.com/football?page=3",
				"http://talksport.com/football?page=4",
				"http://talksport.com/football?page=5",
				"http://talksport.com/football?page=7",
				"http://talksport.com/football?page=8",
				"http://talksport.com/football?page=9",
				"http://talksport.com/football?page=10"]


	def parse(self,response):

		for sel in response.xpath(".//div[contains(@class,'node node-article node-teaser clearfix')]"):
			item = TreBonItem()

			relative_url = sel.xpath(".//a/@href")[0].extract()
			url = response.urljoin(relative_url)

			item['url'] = url
			item['title'] = sel.xpath(".//h2/a/text()")[0].extract()
			item['summary'] = sel.xpath(".//div[contains(@class,'field field-name-field-intro field-type-text-long field-label-hidden')]/div/div/text()")[0].extract()
			item['src'] = 'talksport'
			item['lang'] = 'en'
			yield scrapy.Request(url, callback=self.parse_article,meta={'item': item})

	def parse_article(self, response):
		item = response.meta['item']

		item['image'] = response.xpath(".//div[contains(@class,'field-item even')]/img/@src")[0].extract()
		self.logger.debug('in parse article')
		item['tags'] = response.xpath(".//ul[contains(@class,'links')]/li/a/text()").extract()

		yield item