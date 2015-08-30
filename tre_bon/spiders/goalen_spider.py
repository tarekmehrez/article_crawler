import scrapy
import re
import urllib


from tre_bon.items import GoalENItem
from scrapy.http import HtmlResponse

class GoalENSpider(scrapy.Spider):
	name = 'goal_en'
	allowed_domains = ["goal.com/en"]
	start_urls=["http://www.goal.com/en/news/archive/1"]

	def parse(self,response):
		items =  self.parse_pages(response)
		for item in items:
			yield item

	def parse_pages(self,response):
		items = []
		for sel in response.xpath("//div[contains(@id,'news-archive')]//ul/li"):
			item = {}
			item['head_url'] = response.url
			article_info = sel.xpath(".//div[contains(@class,'articleInfo')]")[0]

			item['title'] = article_info.xpath(".//a/text()")[0].extract()

			item['summary'] = sel.xpath(".//div[contains(@class,'articleSummary')]/text()")[0].extract()
			item['date'] = sel.xpath("../../div[contains(@class,'date')]/text()")[0].extract()
			item['time'] = sel.xpath(".//span")[1].xpath(".//text()")[0].extract()

			url = "http://www.goal.com" + str(article_info.xpath(".//a/@href")[0].extract())
			item['url'] = url

			article_data = urllib.urlopen(url).read()
			article_response = HtmlResponse(url,body=article_data)

			article_items = self.parse_article(article_response)
			if not article_items:
				continue
			item['image'] = article_items[0]

			item['tags'] = []

			item['tags'] = article_items[1]

			tag = str(sel.xpath(".//strong/text()")[0].extract().encode("utf-8"))
			tag = re.sub(r'[^\x00-\x7F]+',' ', tag).replace('-','').strip().lower().replace(' ','_')
			item['tags'].append(tag)

			item['src'] = 'goal_en'
			item['lang'] = 'en'
			items.append(item)


		next_page = response.xpath(".//a[contains(@id,'next-page')]/@href")[0].extract()
		next_page_no = next_page.split('/')[-1]
		next_page_url = "http://www.goal.com" + str(next_page)


		if int(next_page_no) <=5:
			next_data = urllib.urlopen(next_page_url).read()
			next_response = HtmlResponse(next_page_url,body=next_data)
			items += self.parse_pages(next_response)


		return items

	def parse_article(self, response):

		if not response.xpath(".//img[contains(@class,'article-image')]/@src"):
			return(())

		image = response.xpath(".//img[contains(@class,'article-image')]/@src")[0].extract()

		tags = []
		for sel in response.xpath(".//li[contains(@class,'tags')]/a/text()"):
			tag = str(sel.extract().encode('utf-8'))
			tag = re.sub(r'[^\x00-\x7F]+',' ', tag).replace('-','').strip().lower().replace(' ','_')

			tags.append(tag)

		return (image,tags)
