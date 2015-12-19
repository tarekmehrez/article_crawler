# Author: Tarek

now=$(date +%Y-%m-%d:%H:%M:%S)
for spider in $(scrapy list); do
	scrapy crawl $spider 

done
python clusterRelated.py
python updateIndex.py