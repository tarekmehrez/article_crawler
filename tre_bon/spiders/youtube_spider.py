import scrapy
import json
import urllib2

from tre_bon.items import VideoItem


class YoutubeSpider(scrapy.Spider):
	name = 'youtube'
	allowed_domains = ["youtube.com"]
	start_urls = [	"https://www.youtube.com/user/ScoutNationHD/videos",
					"https://www.youtube.com/user/TheFootballDaily/videos",
					"https://www.youtube.com/channel/UC62kbVE2NKaSyF2nRd1KElw/videos",
					"https://www.youtube.com/channel/UCNAf1k0yIjyGu3k9BwAg3lg/videos",
					"https://www.youtube.com/user/HeilRJ03/videos",
					"https://www.youtube.com/user/NikeFootball/videos",
					"https://www.youtube.com/user/fcbarcelona/videos",
					"https://www.youtube.com/user/realmadridcf/videos",
					"https://www.youtube.com/channel/UCmBkHgDND20HOYvV0iaAO7g/videos",
					"https://www.youtube.com/user/mcfcofficial/videos"
					]

	def parse(self,response):

		for sel in response.xpath(".//li[@class='channels-content-item yt-shelf-grid-item']"):
			item = VideoItem()


			relative_url = sel.xpath(".//a/@href")[0].extract()
			url = response.urljoin(relative_url)
			item['type'] = 'video'
			item['url'] = url
			item['title'] = sel.xpath(".//h3/a/@title")[0].extract()

			item['preview_image'] = sel.xpath(".//img/@src")[0].extract().replace("//","")

			if 'ScoutNationHD' in str(response):
				item['src'] = 'youtube:ScoutNationHD'
				item['lang'] = 'en'

			if 'TheFootballDaily' in str(response):
				item['src'] = 'youtube:TheFootballDaily'
				item['lang'] = 'en'

			if 'UC62kbVE2NKaSyF2nRd1KElw' in str(response):
				item['src'] = 'youtube:ArsenalGunner TV'
				item['lang'] = 'en'

			if 'UCNAf1k0yIjyGu3k9BwAg3lg' in str(response):
				item['src'] = 'youtube:Sky Sports Football'
				item['lang'] = 'en'

			if 'HeilRJ03' in str(response):
				item['src'] = 'youtube:HeilRJ'
				item['lang'] = 'en'

			if 'NikeFootball' in str(response):
				item['src'] = 'youtube:Nike Football'
				item['lang'] = 'en'

			if 'fcbarcelona' in str(response):
				item['src'] = 'youtube:FC Barcelona'
				item['lang'] = 'en'


			if 'realmadridcf' in str(response):
				item['src'] = 'youtube:Real Madrid C.F.'
				item['lang'] = 'en'

			if 'UCmBkHgDND20HOYvV0iaAO7g' in str(response):
				item['src'] = 'youtube:Footy MOTD 4'
				item['lang'] = 'en'

			if 'mcfcofficial' in str(response):
				item['src'] = 'youtube:Manchester City FC'
				item['lang'] = 'en'


			yield scrapy.Request(url, callback=self.parse_article,meta={'item': item})



	def parse_article(self, response):
		item = response.meta['item']
		item['date'] = response.xpath(".//strong[@class='watch-time-text']/text()")[0].extract().replace("Published on","")
		item['embed_url'] = item['url'].replace('/watch?v=','/embed/')

		yield item
