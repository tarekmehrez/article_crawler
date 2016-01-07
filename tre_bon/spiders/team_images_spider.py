# Author: Tarek

import scrapy
from tre_bon.items import TeamImageItem



class TeamImagesSpider(scrapy.Spider):
	name = 'team_images'
	allowed_domains = ["en.wikipedia.org"]
	start_urls=["https://en.wikipedia.org/wiki/Category:English_football_logos"
				"https://en.wikipedia.org/wiki/Category:Spanish_football_logos",
				"https://en.wikipedia.org/wiki/Category:German_football_logos",
				"https://en.wikipedia.org/wiki/Category:Italian_football_logos",
				"https://en.wikipedia.org/wiki/Category:Greek_football_logos",
				"https://en.wikipedia.org/wiki/Category:Egyptian_football_logos",
				"https://en.wikipedia.org/wiki/Category:Brazilian_football_logos",
				"https://en.wikipedia.org/wiki/Category:French_football_logos",
				"https://en.wikipedia.org/wiki/Category:Russian_football_logos",
				"https://en.wikipedia.org/wiki/Category:Turkish_football_logos",
				"https://en.wikipedia.org/wiki/Category:Portuguese_football_logos"]


	def parse(self,response):
		for sel in response.xpath(".//div[@class='mw-category']/div/ul/li/a/@href"):
			item = TeamImageItem()
			relative_url = sel.extract()
			url = response.urljoin(relative_url)

			yield scrapy.Request(url, callback=self.parse_article,meta={'item': item})

	def parse_article(self, response):
		item = response.meta['item']
		relative_url = response.xpath(".//div[@class='fullImageLink']/a/img/@src")[0].extract()
		url = response.urljoin(relative_url)

		team_name = response.xpath(".//tr/td/p/a/@title").extract()[0]
		item['url']= url
		item['name']=team_name

		yield item
