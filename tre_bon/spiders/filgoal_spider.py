import scrapy

from tre_bon.items import ArticleItem

class FilGoalSpider(scrapy.Spider):
	name = 'filgoal'
	allowed_domains = ["filgoal.com"]
	start_urls=["http://www.filgoal.com/arabic/allnews.aspx?CatID=1#" + str(i+1) for i in range(20)]


	def parse(self,response):

		for sel in response.xpath(".//div[contains(@class,'AllNews SeeAlso')]/ul/li"):
			item = ArticleItem()
			item['type'] = "article"

			relative_url = sel.xpath(".//a/@href")[0].extract()
			url = response.urljoin(relative_url)

			item['url'] = url
			item['title'] = sel.xpath(".//span[contains(@class,'ANT')]/text()")[0].extract()
			item['summary'] = sel.xpath(".//span[contains(@class,'ANB')]/text()")[0].extract()
			item['src'] = 'filgoal'
			item['lang'] = 'ar'
			item['date'] = sel.xpath(".//div[contains(@class,'ANTInfo')]/span/text()")[0].extract()
			yield scrapy.Request(url, callback=self.parse_article,meta={'item': item})

	def parse_article(self, response):
		item = response.meta['item']
		if response.xpath(".//img[contains(@id,'ctl00_cphFilGoalMain_imgNewsBig')]/@src"):
			item['image'] = response.xpath(".//img[contains(@id,'ctl00_cphFilGoalMain_imgNewsBig')]/@src")[0].extract()
		else:
			item['image'] = response.xpath(".//div[contains(@id,'ctl00_cphFilGoalMain_genImgOrGallery')]/img/@src")[0].extract()
		item['tags'] = response.xpath(".//span[contains(@class,'keywordTag ')]/a/text()").extract()
		content = response.xpath(".//div[contains(@id,'ctl00_cphFilGoalMain_pnlNewsBody')]/p/text()").extract()
		item['content'] = ' '.join(content)
		yield item
