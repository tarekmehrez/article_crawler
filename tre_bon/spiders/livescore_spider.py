import json
import scrapy
from tre_bon.items import LiveScoreItem


class LiveScoreSpider(scrapy.Spider):
	name = 'livescore'
	search_api = 'https://www.googleapis.com/customsearch/v1?key=AIzaSyBDxmhcsZoyWVmiVjrybu4dXcK8aUz54h4&cx=004191593575006642427:exiewnxhrp4&q='
	search_type = '&searchType=image&alt=json'
	allowed_domains = ["football-api.com","google.com","ajax.googleapis.com/"]
	api_key = "16a06f80-781c-b45c-b32623989415"
	start_urls=["http://football-api.com/api/?Action=competitions&APIKey="+api_key]
	DOWNLOAD_DELAY = 0.25  
	def parse(self,response):
		competitions = json.loads(response.body)
		item = LiveScoreItem()
		for competition in competitions["Competition"]:
			item['competition']  = competition['name'] + ' '+competition['region']
			url = self.search_api+item['competition']+' football'+self.search_type
			yield scrapy.Request(url, callback=self.parse_competitionLogo,meta={'item': item,'competition':competition['name'] + ' '+competition['region'],'compId':competition["id"]}, dont_filter=True)

	def parse_competitionLogo(self,response):
		images = json.loads(response.body)
		item = response.meta['item']
		url = 'http://football-api.com/api/?Action=today&APIKey='+self.api_key+'&comp_id=' + response.meta['compId']
		if images['queries']['request'][0]['totalResults']==0:
			item['competitionLogo'] = ''
		else:
			item['competitionLogo'] = images['items'][0]['link']
		yield scrapy.Request(url, callback=self.parse_competition_matches,meta={'item': item,'competition':response.meta['competition']}, dont_filter=True)

	def parse_competition_matches(self,response):
		matches = json.loads(response.body)
		print response.url
		item = response.meta['item']
		if matches['ERROR'] <> 'OK':
			return
		for match in matches['matches']:
			item['competition'] = response.meta['competition']
			item['visitorTeam'] = match['match_visitorteam_name']
			item['visitorTeamScore'] = match['match_visitorteam_score']
			item['localTeam'] = match['match_localteam_name']
			item['localTeamScore'] = match['match_localteam_score']
			item['matchDateTime'] = match['match_formatted_date'].replace('.','-')+' '+match['match_time']
			url = self.search_api+item['localTeam']+' football club'+self.search_type
			yield scrapy.Request(url, callback=self.parse_localTeamLogo,meta={'item': item}, dont_filter=True)

	def parse_localTeamLogo(self,response):
		images = json.loads(response.body)
		item = response.meta['item']
		if images['queries']['request'][0]['totalResults']==0:
			item['localTeamLogo'] = ''
		else:
			item['localTeamLogo'] = images['items'][0]['link']
		url = self.search_api+item['visitorTeam']+' football club'+self.search_type
		yield scrapy.Request(url, callback=self.parse_visitorTeamLogo,meta={'item': item}, dont_filter=True)

	def parse_visitorTeamLogo(self,response):
		images = json.loads(response.body)
		item = response.meta['item']
		if images['queries']['request'][0]['totalResults']==0:
			item['visitorTeamLogo']= ''
		else:
			item['visitorTeamLogo'] = images['items'][0]['link']
		item['src'] = 'livescore'
		item['type'] = 'livescore'
		yield item




	

	
