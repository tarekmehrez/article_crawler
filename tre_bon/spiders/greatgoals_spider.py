import scrapy

from tre_bon.items import TreBonItem

# TODO: handle date format
# TODO: handle endoding and format in tags, summary and titles
# TODO: make sure all tags have similar formats (same tags are grouped)


class GreatGoalspider(scrapy.Spider):
	name = 'greatgoals'
	allowed_domains = ["101greatgoals.com"]
	start_urls=["http://www.101greatgoals.com/blog/page/" + str(i+1) for i in range(10)]


	def parse(self,response):

		for sel in response.xpath(".//li[contains(@class,'cat-blog-container')]"):
			item = TreBonItem()

			url = sel.xpath(".//div[contains(@class,'cat-blog-inner')]/h3/a/@href")[0].extract()

			item['url'] = url
			item['title'] = sel.xpath(".//div[contains(@class,'cat-blog-inner')]/h3/a/text()")[0].extract()
			item['src'] = 'greatgoals'
			item['lang'] = 'en'
			yield scrapy.Request(url, callback=self.parse_article,meta={'item': item})

	def parse_article(self, response):
		item = response.meta['item']
		item['datetime'] = response.xpath(".//div[contains(@class,'post-update updated')]/text()")[0].extract()
		if not response.xpath(".//div[contains(@id,'the-content')]/p/a/@href"):
			return
		item['image'] = response.xpath(".//div[contains(@id,'the-content')]/p/a/@href")[0].extract()
		item['tags'] = response.xpath(".//div[contains(@class,'post-tags')]/a/text()").extract()
		content = response.xpath(".//div[contains(@id,'the-content')]/p/text()").extract()
		item['content'] = ' '.join(content)
		yield item
