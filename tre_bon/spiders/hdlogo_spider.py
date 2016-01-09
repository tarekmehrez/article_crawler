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

				item['url'] = str(sel.xpath(".//dt/a/@href").extract()[0])
				item['name']=str(sel.xpath(".//dd/text()").extract()[0].encode('utf8').strip())

			except:
				continue

			yield item