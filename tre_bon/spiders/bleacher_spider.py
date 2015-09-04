import scrapy
import json
import urllib2

from tre_bon.items import TreBonItem

# TODO: handle endoding and format in tags, summary and titles
# TODO: make sure all tags have similar formats (same tags are grouped)
# TODO: handle date format


class BleacherSpider(scrapy.Spider):
	name = 'bleacher'
	allowed_domains = ["bleacherreport.com"]
	start_urls=["http://bleacherreport.com/world-football"]

	def parse(self, response):


		data = json.load(urllib2.urlopen("http://layser.bleacherreport.com/api/team_stream/world-football?tags=null&limit=100"))
		articles = data['streams'][0]['items']


		for article in articles:
			item = TreBonItem()
			item['title'] = article['title']

			url = article['permalink']

			item['url'] = article['permalink']

			item['image'] = article["primary_image_650x440"]


			item['datetime'] = article["publishedAt"]
			item['src'] = 'bleacher_report'
			item['lang'] = 'en'
			item['tags'] = article['tags']
			yield scrapy.Request(url, callback=self.parse_article,meta={'item': item})


	def parse_article(self,response):
		item = response.meta['item']
		content = response.xpath(".//div[contains(@class,'article_body cf')]/p/text()").extract()
		item['content'] = ' '.join(content)
		yield item