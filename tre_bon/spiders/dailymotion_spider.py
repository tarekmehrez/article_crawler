# Author: Tarek

import scrapy
import json
import urllib2

from tre_bon.items import VideoItem


class DailyMotionSpider(scrapy.Spider):
	name = 'dailymotion'
	allowed_domains = ["dailymotion.com"]
	start_urls=		["http://www.dailymotion.com/user/abuomarlive/" + str(i) for i in range(5)] \
				+	["http://www.dailymotion.com/user/Hadota14/"	+ str(i) for i in range(5)] \
				+	["http://www.dailymotion.com/user/livegoalshd/"	+ str(i) for i in range(5)] \
				+	["http://www.dailymotion.com/user/rubin7190/"	+ str(i) for i in range(5)] \
				+	["http://www.dailymotion.com/user/onlyfootball/"+ str(i) for i in range(5)] \
				+	["http://www.dailymotion.com/user/funnyno1/"	+ str(i) for i in range(5)]

	def parse(self,response):

		for sel in response.xpath(".//div[@class='sd_video_griditem media media-stacked col-4 js-item']"):
			item = VideoItem()


			relative_url =sel.xpath(".//a/@href")[0].extract()
			url = response.urljoin(relative_url)
			item['type'] = 'video'
			item['url'] = url
			item['title'] = sel.xpath(".//img/@title")[0].extract()

			item['preview_image'] = sel.xpath(".//div/@data-spr")[0].extract()

			if 'abuomar' in str(response):
				item['src'] = 'dailymotion:abuomarlive'
				item['lang'] = 'ar'

			if 'Hadota14' in str(response):
				item['src'] = 'dailymotion:korabia'
				item['lang'] = 'ar'

			if 'livegoalshd' in str(response):
				item['src'] = 'dailymotion:GoalsHD'
				item['lang'] = 'en'

			if 'rubin7190' in str(response):
				item['src'] = 'dailymotion:Football Highlights'
				item['lang'] = 'en'

			if 'onlyfootball' in str(response):
				item['src'] = 'dailymotion:Only Football'
				item['lang'] = 'en'

			if 'funnyno1' in str(response):
				item['src'] = 'dailymotion:funnyno1'
				item['lang'] = 'en'

			yield scrapy.Request(url, callback=self.parse_article,meta={'item': item})



	def parse_article(self, response):
		item = response.meta['item']
		item['date'] =  response.xpath(".//li[@class='mrg-btm-xs']/text()")[1].extract()

		data = json.load(urllib2.urlopen("http://www.dailymotion.com/api/oembed?url="+item['url']))
		item['embed_code'] = data['html']

		yield item
