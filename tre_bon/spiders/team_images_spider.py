# Author: Tarek

import scrapy
from tre_bon.items import TeamImageItem



class TeamImagesSpider(scrapy.Spider):
	name = 'team_images'
	allowed_domains = ["en.wikipedia.org"]
	leagues=[	'English_football_logos',
				'Spanish_football_logos',
				'German_football_logos',
				'Italian_football_logos',
				'Greek_football_logos',
				'Egyptian_football_logos',
				'Brazilian_football_logos',
				'French_football_logos',
				'Russian_football_logos',
				'Turkish_football_logos',
				'Portuguese_football_logos']
	start_urls=["https://en.wikipedia.org/wiki/Category:" + leauge for leauge in leagues ]


	def parse(self,response):
		for sel in response.xpath(".//div[@class='mw-category']/div/ul/li/a/@href"):
			item = TeamImageItem()
			item['type']='team_logo'
			item['src']='wikipedia'
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
