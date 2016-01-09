# Author: Tarek

import scrapy
from tre_bon.items import TeamImageItem



class HDLogo(scrapy.Spider):
	name = 'hdlogo'
	allowed_domains = ["hdlogo.wordpress.com"]
	start_urls=["https://hdlogo.wordpress.com/page/" + str(i) for i in range(1,7)]

	def parse(self,response):
		for sel in response.xpath(".//dl[@class='gallery-item']"):
			item = TeamImageItem()
			item['type']='team_logo'
			item['src']='hdlogo'
			try:
				item['name']=str(sel.xpath(".//dd/text()").extract()[0].encode('utf8').strip())
				yield scrapy.Request(str(sel.xpath(".//dt/a/@href").extract()[0]), callback=self.get_image,meta={'item': item}, dont_filter=True)

			except:
				continue

	def get_image(self,response):
		item = response.meta['item']
		item['image'] = str(response.xpath('//p[contains(@class,"attachment")]//img/@src').extract()[0])
		yield item