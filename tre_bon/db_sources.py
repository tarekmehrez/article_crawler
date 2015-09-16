import pymongo

try:
    conn=pymongo.MongoClient('localhost', 27017)
    print "Connected successfully!!!"
except pymongo.errors.ConnectionFailure, e:
   print "Could not connect to MongoDB: %s" % e

db = conn.tre_bon
sources = db.sources

if sources.count() == 0:
	sources.insert({"name": "bein_en", 	"lang": "en", "type": "articles", "feed_items": []})
	sources.insert({"name": "bleacher", "lang": "en", "type": "articles", "feed_items": []})
	sources.insert({"name": "cairokora","lang": "ar", "type": "articles", "feed_items": []})
	sources.insert({"name": "espn", 	"lang": "en", "type": "articles", "feed_items": []})
	sources.insert({"name": "fifa_ar", 	"lang": "ar", "type": "articles", "feed_items": []})
	sources.insert({"name": "fifa_en", 	"lang": "en", "type": "articles", "feed_items": []})
	sources.insert({"name": "filgoal", 	"lang": "ar", "type": "articles", "feed_items": []})
	sources.insert({"name": "goal_en", 	"lang": "en", "type": "articles", "feed_items": []})
	sources.insert({"name": "goal_ar", 	"lang": "ar", "type": "articles", "feed_items": []})
	sources.insert({"name": "hihi2", 	"lang": "ar", "type": "articles", "feed_items": []})
	sources.insert({"name": "skysports","lang": "en", "type": "articles", "feed_items": []})
	sources.insert({"name": "talksport","lang": "en", "type": "articles", "feed_items": []})
	sources.insert({"name": "yallakora","lang": "ar", "type": "articles", "feed_items": []})

