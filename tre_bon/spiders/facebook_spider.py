import json
import scrapy
from tre_bon.items import ArticleItem

class FacebookSpider(scrapy.Spider):
	name = 'facebook'
	allowed_domains = ["facebook.com"]
	access_token ="806885982764632|vVnxQ2H9Zu29sYmx9lQl_HxVLH0"
	post_limit = 30
	apiLink ="https://graph.facebook.com/v2.5/"
	pages = ["Cristiano","LeoMessi","ThierryHenry","andreapirlopaginaufficiale","Iker.Casillas","mesutoezil","edenhazard","ZlatanIbrahimovic","Beckham","Kaka","10Jamesrodriguez","manuel.neuer","alexissanchez7","neymarjr","momosalah","Bale","soccerbible","footballdaily","SquawkaFootball","mirrorfootball","GoalUK","BBCMOTD","guardianfootball"]
	start_urls=[apiLink+page_id+"/posts?limit="+str(post_limit)+"&fields=id,type,created_time,name,message,link,from&access_token=" + access_token for page_id in pages]
	def parse(self,response):
		posts = json.loads(response.body)
		itemCount = 1
		for post in posts["data"]:
			item = ArticleItem()
			item['type'] ="article" #needs to be checked
			url = post['link']
			item['postId'] = self.name+post['id']
			item['url'] = url
			item['tags'] = ' '
			item['title'] = post['from']["name"]
			if 'message' in post:
				item['summary'] = post['message']
			else:
				item['summary'] = ' '
			item['src'] = 'facebook'
			item['lang'] = 'en'
			item['account_image'] = 'https://graph.facebook.com/'+post['id'].split('_')[0]+'/picture?type=normal&access_token='+self.access_token #post["picture"]

			item['date'] = post["created_time"]

			item['content'] = item['summary']
			item['itemIndex'] = itemCount
			itemCount = itemCount+1
			isLink =  False
			if post['type']=='photo':
				item['image'] ='https://graph.facebook.com/'+post['id'].split('_')[-1]+'/picture?type=normal&access_token='+self.access_token #post["picture"]
			elif post['type']=='link' or ('facebook.com' not in url and 'fbcdn' not in url):
				item['image'] = ''
				isLink = True
				yield scrapy.Request(url, callback=self.parse_link,meta={'item': item},dont_filter=True)
			else:
				item['image'] = ''
			if isLink==False:
				yield item
	def parse_link(self,response):
		item = response.meta['item']
		url = response.url
		image_url = response.xpath('//meta[@property="og:image"]/@content').extract()
		image_tag = ''
		if len(image_url)>0:
			image_url = image_url[0]
			item['image'] = image_url
			#image_tag = '<br><img ng-src="images/loading-icon.gif" ng-click="'+url+'" lazy-img="'+image_url+'" /><br>'
		#outTag = image_tag+'<a href="'+url+'">Continue Reading</a>'
		#item['summary'] = item['summary']+' '+outTag
		yield item
