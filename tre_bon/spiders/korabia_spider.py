import scrapy

from tre_bon.items import ArticleItem


class KorabiaSpider(scrapy.Spider):
	name = 'korabia'
	allowed_domains = ["korabia.com"]
	start_urls = ["http://www.korabia.com/News?page=" + str(i+1) for i in range(10)]


	def parse(self,response):

		for sel in response.xpath(".//div[starts-with(@class,'news_box')]"):
			item = ArticleItem()
			item['type'] = "article"

			relative_url = sel.xpath(".//a/@href")[0].extract()
			url = response.urljoin(relative_url)
			item['url'] = url
			item['title'] = sel.xpath(".//h2/a/text()")[0].extract()


			item['summary'] = sel.xpath(".//h3/text()")[0].extract()
			item['src'] = 'korabia'
			item['lang'] = 'ar'
			item['date'] = sel.xpath(".//h4/text()")[0].extract()

			yield scrapy.Request(url, callback=self.parse_article,meta={'item': item})


	def parse_article(self, response):
		item = response.meta['item']
		item['image'] = response.xpath(".//div[@class='details_img']/img/@src")[0].extract()

		content = response.xpath(".//div[@class='fontt']/p/text()").extract()
		item['content'] = ' '.join(content)


		yield item
