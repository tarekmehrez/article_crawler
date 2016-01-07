import json
import scrapy
from tre_bon.items import ArticleItem

class FacebookSpider(scrapy.Spider):
	name = 'facebook'
	allowed_domains = ["facebook.com"]
	access_token ="CAACEdEose0cBAAl0tl28aP7B7GhCNpUiKZAdS4w2E0u6NhGPGSIPr4vMW5IjoG4A5ZBZCoYIWcM1Ih5XfZAQZAZBtZCB8RZATfU7PeJMvM8CA33SU52PxsDQZCOToA2sUkq36jq5gEycgvBMnM2FbXjI6YoCe3bFrAfBfkrTcEPxWRWdSkZCgLc7sU9FTdRhL9OsOkUiTB2uZAy7CIEUuAmF1wP"
	post_limit = 30
	apiLink ="https://graph.facebook.com/v2.2/"
	pages = ["Cristiano","LeoMessi","ThierryHenry","andreapirlopaginaufficiale","Iker.Casillas","mesutoezil","edenhazard","ZlatanIbrahimovic","Beckham","Kaka","10Jamesrodriguez","manuel.neuer","alexissanchez7","neymarjr","momosalah","Bale","soccerbible","footballdaily","SquawkaFootball","mirrorfootball","GoalUK","BBCMOTD","guardianfootball"]
	start_urls=[apiLink+page_id+"/posts?limit="+str(post_limit)+"&access_token=" + access_token for page_id in pages]
	def parse(self,response):
		posts = json.loads(response.body)
		itemCount = 1
		for post in posts["data"]:
			item = ArticleItem()
			item['type'] ="article" #needs to be checked
			url = post["actions"][0]['link']
			item['postId'] = self.name+post['id']
			item['url'] = url
			item['tags'] = ' '
			item['title'] = post['from']["name"]
			item['summary'] = post['message']
			item['src'] = 'facebook'
			item['lang'] = 'en'
			item['image'] = 'https://graph.facebook.com/'+post['id'].split('_')[-1]+'/picture?type=normal&access_token='+self.access_token #post["picture"]
			item['account_image'] = 'https://graph.facebook.com/'+post['id'].split('_')[0]+'/picture?type=normal&access_token='+self.access_token #post["picture"]

			item['date'] = post["created_time"]

			if post["type"]=="link":
				item['content'] = post["message"] +" <a href='"+post["link"]+"'>"+post["link"]+"</a>"
			else:
				item['content'] = item['summary']
			item['itemIndex'] = itemCount
			itemCount = itemCount+1
			yield item
