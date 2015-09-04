import scrapy

from tre_bon.items import TreBonItem


# TODO: handle date format
# TODO: handle endoding and format in tags, summary and titles
# TODO: make sure all tags have similar formats (same tags are grouped)


class YallaKoraSpider(scrapy.Spider):
	name = 'yallakora'
	allowed_domains = ["yallakora.com"]
	start_urls=["http://www.yallakora.com/News/LoadMoreCategory.aspx?page=1&newsregion=1&type=26",
				"http://www.yallakora.com/News/LoadMoreCategory.aspx?page=2&newsregion=1&type=26",
				"http://www.yallakora.com/News/LoadMoreCategory.aspx?page=3&newsregion=1&type=26",
				"http://www.yallakora.com/News/LoadMoreCategory.aspx?page=4&newsregion=1&type=26",
				"http://www.yallakora.com/News/LoadMoreCategory.aspx?page=5&newsregion=1&type=26",
				"http://www.yallakora.com/News/LoadMoreCategory.aspx?page=6&newsregion=1&type=26",
				"http://www.yallakora.com/News/LoadMoreCategory.aspx?page=7&newsregion=1&type=26",
				"http://www.yallakora.com/News/LoadMoreCategory.aspx?page=8&newsregion=1&type=26",
				"http://www.yallakora.com/News/LoadMoreCategory.aspx?page=9&newsregion=1&type=26",
				"http://www.yallakora.com/News/LoadMoreCategory.aspx?page=10&newsregion=1&type=26",
				"http://www.yallakora.com/News/LoadMoreCategory.aspx?page=2&newsregion=1&type=1",
				"http://www.yallakora.com/News/LoadMoreCategory.aspx?page=3&newsregion=1&type=1",
				"http://www.yallakora.com/News/LoadMoreCategory.aspx?page=4&newsregion=1&type=1",
				"http://www.yallakora.com/News/LoadMoreCategory.aspx?page=5&newsregion=1&type=1",
				"http://www.yallakora.com/News/LoadMoreCategory.aspx?page=6&newsregion=1&type=1",
				"http://www.yallakora.com/News/LoadMoreCategory.aspx?page=7&newsregion=1&type=1",
				"http://www.yallakora.com/News/LoadMoreCategory.aspx?page=8&newsregion=1&type=1",
				"http://www.yallakora.com/News/LoadMoreCategory.aspx?page=9&newsregion=1&type=1",
				"http://www.yallakora.com/News/LoadMoreCategory.aspx?page=10&newsregion=1&type=1",
				"http://www.yallakora.com/News/LoadMoreCategory.aspx?page=1&newsregion=1&type=1"]


	def parse(self,response):

		for sel in response.xpath(".//li[contains(@class,'ClipItem')]"):
			item = TreBonItem()

			relative_url = sel.xpath(".//a[contains(@class,'NewsTitle')]/@href")[0].extract()
			url = response.urljoin(relative_url)

			item['url'] = url
			item['title'] = sel.xpath(".//a[contains(@class,'NewsTitle')]/text()")[0].extract().strip()
			item['src'] = 'yallkora'
			item['lang'] = 'ar'
			yield scrapy.Request(url, callback=self.parse_article,meta={'item': item})

	def parse_article(self, response):
		item = response.meta['item']

		item['image'] = response.xpath(".//div[contains(@class,'ArticleIMG')]/img/@src")[0].extract().strip()
		if response.xpath(".//span[contains(@class,'PortfolioDate')]/text()"):
			item['datetime'] = response.xpath(".//span[contains(@class,'PortfolioDate')]/text()")[0].extract().strip()
		item['tags'] = response.xpath(".//ul[contains(@class,'TourTabs floatRight')]/li/a/span/text()").extract()
		content=   response.xpath(".//div[contains(@class,'articleBody')]/text()").extract()
		item['content'] = ' '.join(content)
		yield item
