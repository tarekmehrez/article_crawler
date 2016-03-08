# Author: Tarek

import cPickle
import scrapy
import os.path

from instagram.client import InstagramAPI
from tre_bon.items import InstagramItem



class InstagramSpider(scrapy.Spider):

	name = 'instagram'

	allowed_domains = ["instagram.com"]
	start_urls = ["http://www.instagram.com"]

	def __init__(self):
		access_token ="182023789.04c8e57.9e150e8ccd49440d96b7e3b0cf53179f"
		self.api = InstagramAPI(access_token=access_token,client_secret="85ecfb407c34423c8efcf82af4b38695")


		self.user_ids = {}
		self.user_imgs = {}

					# players
		accounts = ['cristiano', 'leomessi', 'waynerooney', 'zidane', 'iamzlatanibrahimovic', 'toni.kr8s', 'davidluiz_4', 'hazardeden_10', 'davidbeckham', 'andreapirlo21thierryhenry', 'luissuarez9', 'garethbale11', 'andresiniesta8', 'neymarjr', 'kingarturo23oficial', 'manuelneuer', 'didierdrogba', 'mosalah22', 'ronaldolima', 'kaka', 'm10_official', 'jamesrodriguez10', 'ikercasillasoficial', 'mb459', 'marcelotwelve', 'alexis_officia1', 'stevengerrard', 'realmadrid', 'fcbarcelona', 'chelseafc', 'arsenal', 'liverpoolfc', 'manchesterunited', 'mcfcofficial', 'juventus', 'officialasroma', 'inter', 'acmilan', 'acffiorentina', 'psg', 'fcbayern', 'bvb09', 'uefachampionsleague', 'instareplays', 'robgunillustration', 'squawkafootball', 'soccermemes', 'futbolsport', 'nikefootball', 'pumafootball', 'adidasfootball', 'instareplays', '6secfootball101greatgoals', '8fact_football', 'premierleague', 'laliga', 'espnfc', 'beinsports', 'bestoffootball', 'golazoweekly', 'worldgoalz', 'futbol_evolution', 'footballtransfersdailywe_love_football', 
					'footbalita', '8factfootball', 'football.news', 'footykix', 'yallakoraofficial', 'filgoal1', 'talksport', 'kooora', 
					'cristiano','leomessi', 'waynerooney','zidane','iamzlatanibrahimovic', 'toni.kr8s','davidluiz_4',
					'hazardeden_10','davidbeckham','andreapirlo21',
					'thierryhenry','luissuarez9','garethbale11','andresiniesta8','neymarjr','kingarturo23oficial','manuelneuer','didierdrogba','mosalah22',
					'ronaldolima','kaka','m10_official','jamesrodriguez10','ikercasillasoficial','mb459','marcelotwelve','alexis_officia1','stevengerrard',
					# clubs
					'realmadrid','fcbarcelona',
					'chelseafc','arsenal','liverpoolfc','manchesterunited','mcfcofficial',
					'juventus','officialasroma','inter','acmilan','acffiorentina',
					'psg',
					'fcbayern','bvb09',
					# other accounts
					'433','visubal','officialfootballmemes', 'instatroll_football'
					'uefachampionsleague','instareplays','robgunillustration','squawkafootball','soccermemes','futbolsport','nikefootball','pumafootball','adidasfootball','instareplays','6secfootball',
					'101greatgoals','8fact_football','premierleague','laliga','espnfc','beinsports','bestoffootball','golazoweekly','worldgoalz','futbol_evolution','footballtransfersdaily',
					'we_love_football','footbalita','8factfootball','football.news','footykix','yallakoraofficial','filgoal1','talksport','kooora']


		if not ( os.path.exists('insta_user_ids.pickle') and os.path.exists('insta_user_imgs.pickle')):
			accounts = list(set(accounts))
			for account in accounts:
				print 'looking for: ', account
				user_list = self.api.user_search(account)
				print user_list
				if user_list:
					for user in user_list:
						if user.username == account:
							self.user_ids[account] = user.id
							self.user_imgs[account] = user.profile_picture
							print 'found: ', user

			with open('insta_user_ids.pickle', 'wb') as f:
				cPickle.dump(self.user_ids, f)

			with open('insta_user_imgs.pickle', 'wb') as f:
				cPickle.dump(self.user_imgs, f)

		else:
			with open('insta_user_ids.pickle', 'r') as f:
				self.user_ids = cPickle.load(f)

			with open('insta_user_imgs.pickle', 'r') as f:
				self.user_imgs = cPickle.load(f)

	def parse(self,response):
		itemCount  = 1
		for user in self.user_ids:
			self.logger.debug("Retrieving data for " + str(user))
			recent_media, next_ = self.api.user_recent_media(user_id=self.user_ids[user])
			for media in recent_media:
				item = InstagramItem()

				if media.caption:
					item['caption'] = media.caption.text
				item['lang'] = 'en'
				item['date'] = media.created_time
				item['src'] = 'instagram'
				item['account'] = user
				item['account_image'] = self.user_imgs[user]

				item['tags'] = []
				for tag in media.tags:
					item['tags'].append(str(tag).split(' ')[1])

				item['url'] = media.link
				item['type'] = media.type

				if media.type == 'image':
					item['img_vid_src'] = media.images['standard_resolution'].url
				else:
					item['img_vid_src'] = media.videos['standard_resolution'].url

				item['likes'] = media.like_count
				item['media_id'] = media.id
				item['itemIndex'] = itemCount
				itemCount = itemCount+1

				yield item
