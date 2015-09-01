import scrapy

from tre_bon.items import GreatGoalsItem

# TODO: handle date format
# TODO: handle endoding and format in tags, summary and titles
# TODO: make sure all tags have similar formats (same tags are grouped)


class GreatGoalspider(scrapy.Spider):
	name = 'greatgoals'
	allowed_domains = ["101greatgoals.com"]
	start_urls=["http://www.101greatgoals.com/blog/",
				"http://www.101greatgoals.com/blog/page/2/",
				"http://www.101greatgoals.com/blog/page/3/",
				"http://www.101greatgoals.com/blog/page/4/",
				"http://www.101greatgoals.com/blog/page/5/",
				"http://www.101greatgoals.com/blog/page/6/",
				"http://www.101greatgoals.com/blog/page/7/",
				"http://www.101greatgoals.com/blog/page/8/",
				"http://www.101greatgoals.com/blog/page/9/",
				"http://www.101greatgoals.com/blog/page/10/"]


	def parse(self,response):

		for sel in response.xpath(".//li[contains(@class,'cat-blog-container')]"):
			item = GreatGoalsItem()

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
		yield item
