import pymongo
import random
import numpy as np

from datetime import datetime, timedelta


try:
	conn=pymongo.MongoClient('localhost', 27017)
except pymongo.errors.ConnectionFailure, e:
	print "Could not connect to MongoDB: %s" % e


db = conn.tre_bon
feed_items = db.feed_items


date = datetime.now()-timedelta(days=3)

timeline = list(feed_items.find({'date':{'$gt':date}}).sort([("date", pymongo.DESCENDING)]))
final_timeline = []

splits = np.array_split(timeline,len(timeline)/50)
for split in splits:
	np.random.shuffle(split)
	np.random.shuffle(split)
	np.random.shuffle(split)
	final_timeline += split.tolist()

