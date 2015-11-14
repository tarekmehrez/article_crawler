import json
import scrapy
from tre_bon.items import LiveScoreItem

class LiveScoreSpider(scrapy.Spider):
	name = 'livescore'
	allowed_domains = ["football-api.com","google.com","ajax.googleapis.com/"]
	api_key = "16a06f80-781c-b45c-b32623989415"
	start_urls=["http://football-api.com/api/?Action=competitions&APIKey="+api_key]
	DOWNLOAD_DELAY = 0.25  
	def parse(self,response):
		competitions = json.loads(response.body)
		item = LiveScoreItem()
		for competition in competitions["Competition"]:
			item['competition']  = competition['name'] + ' '+competition['region']
			url = 'https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q='+item['competition']+' football'
			yield scrapy.Request(url, callback=self.parse_competitionLogo,meta={'item': item,'compId':competition["id"]}, dont_filter=True)

	def parse_competitionLogo(self,response):
		images = json.loads(response.body)
		item = response.meta['item']
		url = 'http://football-api.com/api/?Action=today&APIKey='+self.api_key+'&comp_id=' + response.meta['compId']
		item['competitionLogo'] = images['responseData']['results'][0]['url']
		yield scrapy.Request(url, callback=self.parse_competition_matches,meta={'item': item}, dont_filter=True)

	def parse_competition_matches(self,response):
		matches = json.loads(response.body)
		print response.url
		item = response.meta['item']
		if matches['ERROR'] <> 'OK':
			return
		for match in matches['matches']:
			item['visitorTeam'] = match['match_visitorteam_name']
			item['visitorTeamScore'] = match['match_visitorteam_score']
			item['localTeam'] = match['match_localteam_name']
			item['localTeamScore'] = match['match_localteam_score']
			item['matchDateTime'] = match['match_formatted_date'].replace('.','-')+' '+match['match_time']
			url = 'https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q='+item['localTeam']+' football club'
			yield scrapy.Request(url, callback=self.parse_localTeamLogo,meta={'item': item}, dont_filter=True)

	def parse_localTeamLogo(self,response):
		images = json.loads(response.body)
		item = response.meta['item']
		item['localTeamLogo'] = images['responseData']['results'][0]['url']
		url = 'https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q='+item['visitorTeam']+' football club'
		yield scrapy.Request(url, callback=self.parse_visitorTeamLogo,meta={'item': item}, dont_filter=True)

	def parse_visitorTeamLogo(self,response):
		images = json.loads(response.body)
		item = response.meta['item']
		item['visitorTeamLogo'] = images['responseData']['results'][0]['url']
		item['src'] = 'livescore'
		item['type'] = 'livescore'
		yield item




	

	
