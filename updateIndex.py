# Author: Mostafa ElAraby
#used to update item index used for the timeline
import pymysql
def updateIndex(tableName):
	if tableName=='articles':
		cur.execute('SELECT articles.src as src FROM articles group by articles.src;')
		articlesSrc = cur.fetchall()
		for src in articlesSrc:
			cur.execute('SELECT id FROM articles WHERE src=%s order by date desc;',(src[0]))
			articles = cur.fetchall()
			currentItemIndex = 0
			updateQuery = '';
			if len(articles):
				print 'error '+tableName
				return
			for  article in articles:
				updateQuery += 'update articles set itemIndex='+str(currentItemIndex)+' where id='+str(article[0])+'; '
				currentItemIndex = currentItemIndex+1
			cur.execute(updateQuery)
	else:
		cur.execute('SELECT id FROM '+tableName+'  order by date desc;')
		posts = cur.fetchall()
		if len(posts)==0:
			print 'error '+tableName
			return
		currentItemIndex = 0
		updateQuery = ''
		for post in posts:
			updateQuery+='update '+tableName+' set itemIndex='+str(currentItemIndex)+' where id='+str(post[0])+'; '
			currentItemIndex = currentItemIndex+1
		cur.execute(updateQuery)
	db.commit()

db =  pymysql.connect(host='localhost', # your host, usually localhost
                     user='root', # your username
                      passwd='', # your password
                      db='threebont') # name of the data base
db.set_charset('utf8')
cur = db.cursor()
updateIndex('articles')
updateIndex('videos')
updateIndex('twitter')
updateIndex('instagram')

