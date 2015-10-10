import json
import scrapy
from tre_bon.items import ArticleItem

class FacebookSpider(scrapy.Spider):
	name = 'facebook'
	allowed_domains = ["facebook.com"]
	access_token =""#needs access token
	post_limit = 5
	apiLink ="https://graph.facebook.com/v2.2/"
	pages = ["Cristiano","LeoMessi","ThierryHenry","andreapirlopaginaufficiale","Iker.Casillas","mesutoezil","edenhazard","ZlatanIbrahimovic","Beckham","Kaka","10Jamesrodriguez","manuel.neuer","alexissanchez7","neymarjr","momosalah","Bale","soccerbible","footballdaily","SquawkaFootball","mirrorfootball","GoalUK","BBCMOTD","guardianfootball"]
	start_urls=[apiLink+page_id+"/posts?limit="+str(post_limit)+"&access_token=" + access_token for page_id in pages]
	def parse(self,response):
		posts = json.loads(response.body)
		for post in posts["data"]:
			item = ArticleItem()
			item['type'] ="article" #needs to be checked
			url = post["actions"][0]['link']
			item['url'] = url
			item['title'] = post["name"]
			item['summary'] = post["description"]
			item['src'] = 'facebook'
			item['lang'] = 'en'
			item['image'] = post["picture"]
			item['date'] = post["created_time"]
			if post["type"]=="link":
				item['content'] = post["description"] +" <a href='"+post["link"]+"'>"+post["link"]+"</a>"
			else:
				item['content'] = item['description']
			yield item
