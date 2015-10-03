# Author: Tarek

import scrapy

from tre_bon.items import ArticleItem



class FifaARSpider(scrapy.Spider):
	name = 'fifa_ar'
	allowed_domains = ["fifa.com"]
	start_urls=["http://ar.fifa.com/news/library/all-news/index,page=" + str(i+1) + ".htmx" for i in range(5)]



	def parse(self,response):

		for sel in response.xpath(".//li[contains(@class,'dcm-thumblist-item')]"):
			item = ArticleItem()
			item['type'] = "article"

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

		if response.xpath(".//time/@date"):
			item['date'] = response.xpath(".//time/@date")[0].extract()
		content = response.xpath(".//div[contains(@class,'article-body')]/p/text()").extract()
		if not content:
			content = response.xpath(".//div[@class=' articleBody  landscapePh ']/p/text()").extract()

		item['content'] = ' '.join(content)
		yield item
