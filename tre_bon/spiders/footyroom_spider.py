# Author: Mostafa ElAraby

import scrapy
import json
import urllib2
import re
from tre_bon.items import VideoItem

class FootyRoomSpider(scrapy.Spider):
	name = 'footyroom'
	allowed_domains = ["footyroom.com"]
	start_urls=["http://footyroom.com/api/2.0/posts.php?page=" + str(i+1)+"&categoryId=34" for i in range(1)]

	itemCount = 1
	def parse(self,response):
		account_image = 'http://cdn.footyroom.com/pics/logo.png'
		for sel in response.xpath("//div[contains(@class,'vid')]"):
			item = VideoItem()
			relative_url = sel.xpath(".//header/a/@href").extract()
			if len(relative_url)==0:
				continue
			relative_url = relative_url[0]
			url = response.urljoin(relative_url)
			item['type'] = 'video'
			item['url'] = url
			item['account_image'] = account_image
			item['title'] = sel.xpath(".//header/a/text()")[0].extract()
			item['preview_image'] = sel.xpath(".//div[contains(@class,'vidthumb')]/a/img/@src")[0].extract()
			item['src'] = 'footyroom'
			item['itemIndex'] = self.itemCount
			item['channel'] = ' '
			item['lang'] = 'en'
			item['date'] = sel.xpath(".//footer/span/text()")
			yield scrapy.Request(url, callback=self.parse_video,meta={'item': item})
	def parse_video(self,response):
		item = response.meta['item']
		currentScript = response.xpath("//div[contains(@class,'video-section')]/script/text()")[0].extract().strip()
		embed_url = re.search(r'(https:.*) f',currentScript)
		print currentScript
		if embed_url:
			embed_url = embed_url.group(1).replace("\\","")
		else:
			return
		item['embed_url'] = embed_url
		item['embed_code'] = '<iframe width="560" height="315" src="'+item['embed_url']+'" frameborder="0" allowfullscreen></iframe>'

		yield item