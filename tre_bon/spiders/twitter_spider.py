# Author: Tarek

import tweepy
import scrapy

from tre_bon.items import TwitterItem


class TwitterSpider(scrapy.Spider):

	name = 'twitter'

	allowed_domains = ["twitter.com"]
	start_urls = ["http://www.twitter.com"]

	def __init__(self):
		consumer_key = 't1zIAmDAW0ay1vYP2E8lR0cXu'
		consumer_secret = 'VXoUJYRHxEcBM39KGvHciHeGaLilHaD2zKgCR1lvZE8nvdUqB8'

		access_token = '156821840-nvhu18pl053GLpygCOkMK8gnwyEMG1c74wWumMcl'
		access_token_secret = 'CRaLLhtyj62RNSmzSGCcWZJ0YCkAh0F4Kk84RYW3Kc7wo'

		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)

		self.api = tweepy.API(auth)

		self.accounts = [	'UberFootbalI', 'Troll__Football', 'TransferSources','Footy_Jokes', 'Footy_WAGs','FootballFunnys',
							'FootyHumour','DirtyFootbaIIer','_fantasypremier','Football__Tweet','LaughingFooty','8Fact_Footballl',
							'Cristiano','rioferdy5','WayneRooney', 'GNev2','RobHarris','GaryLineker',
							'FCBarcelona','ChelseaFC','ManUtd','Arsenal','LFC','MCFC',
							'Squawka','BBCSport','GeniusFootball', 'premierleague','MirrorFootball']


	def parse(self,response):
		itemCount = 1
		for account in self.accounts:
			self.logger.debug("Retrieving data for " + str(account))
			tweets = self.api.user_timeline(account)

			for tweet in tweets:

				item = TwitterItem()
				item['itemIndex'] = itemCount
				itemCount = itemCount+1
				item['lang'] = tweet.lang
				item['text'] = tweet.text
				item['tags'] = ''
				item['src'] = 'twitter'
				item['account'] = tweet.user.name
				item['account_image'] = tweet.user.profile_image_url

				if len(tweet.entities['hashtags']) > 0:
					item['tags'] = []
					for tag in tweet.entities['hashtags']:
						item['tags'].append(tag['text'])

				item['date'] =  tweet.created_at
				item['url'] =  "https://twitter.com/" + str(tweet.user.screen_name) + "/status/" + str(tweet.id)
				item['media_url'] = ''
				if 'media' in tweet.entities:
					item['media_url'] = 'https://'+tweet.entities['media'][0]['media_url_https']

				item['retweets'] = tweet.retweet_count
				item['favs'] = tweet.favorite_count
				item['tweet_id'] = tweet.id
				yield item