import scrapy

from datetime import datetime
from tre_bon.items import TreBonItem


# TODO: handle date format
# TODO: handle endoding and format in tags, summary and titles
# TODO: make sure all tags have similar formats (same tags are grouped)


class FifaENSpider(scrapy.Spider):
	name = 'fifa_en'
	allowed_domains = ["fifa.com"]
	start_urls=["http://www.fifa.com/news/library/all-news/index,page=1.htmx",
				"http://www.fifa.com/news/library/all-news/index,page=2.htmx",
				"http://www.fifa.com/news/library/all-news/index,page=3.htmx",
				"http://www.fifa.com/news/library/all-news/index,page=4.htmx",
				"http://www.fifa.com/news/library/all-news/index,page=5.htmx",
				"http://www.fifa.com/news/library/all-news/index,page=6.htmx",
				"http://www.fifa.com/news/library/all-news/index,page=7.htmx",
				"http://www.fifa.com/news/library/all-news/index,page=8.htmx",
				"http://www.fifa.com/news/library/all-news/index,page=9.htmx",
				"http://www.fifa.com/news/library/all-news/index,page=10.htmx"
				"http://www.fifa.com/news/library/all-news/index,page=11.htmx",
				"http://www.fifa.com/news/library/all-news/index,page=12.htmx",
				"http://www.fifa.com/news/library/all-news/index,page=13.htmx",
				"http://www.fifa.com/news/library/all-news/index,page=14.htmx",
				"http://www.fifa.com/news/library/all-news/index,page=15.htmx",
				"http://www.fifa.com/news/library/all-news/index,page=16.htmx",
				"http://www.fifa.com/news/library/all-news/index,page=17.htmx",
				"http://www.fifa.com/news/library/all-news/index,page=18.htmx",
				"http://www.fifa.com/news/library/all-news/index,page=19.htmx",
				"http://www.fifa.com/news/library/all-news/index,page=20.htmx"]

	def __init__(self):
		self.datetime=''

	def parse(self,response):

		for sel in response.xpath(".//li[contains(@class,'dcm-thumblist-item')]"):
			item = TreBonItem()

			relative_url = sel.xpath(".//h4/a/@href")[0].extract()
			url = response.urljoin(relative_url)

			item['url'] = url
			item['title'] = sel.xpath(".//h4/a/text()")[0].extract()
			item['summary'] = sel.xpath(".//img/@ph-data-picture-comment")[0].extract()
			item['src'] = 'fifa'
			item['lang'] = 'ar'
			item['image'] = sel.xpath(".//img/@ph-data-picture-url")[0].extract()
			yield scrapy.Request(url, callback=self.parse_article,meta={'item': item})

	def parse_article(self, response):
		item = response.meta['item']

		if response.xpath(".//time/@datetime"):
			item['datetime'] = response.xpath(".//time/@datetime")[0].extract()
			self.datetime = item['datetime']
		else:
			if not self.datetime:
				item['datetime'] = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
			else:
				item['datetime'] = self.datetime
		content = response.xpath(".//div[contains(@class,'article-body')]/p/text()").extract()
		item['content'] = ' '.join(content)
		yield item
