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
