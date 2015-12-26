# Author: Tarek

now=$(date +%Y-%m-%d:%H:%M:%S)
cd /var/crawlers/article_crawler
echo "Starting cron activity at $now, please wait..." > /var/crawlers/article_crawler/l$

cuttoff=$1
for spider in $(scrapy list | head -$1 | tail -6); do
        scrapy crawl $spider

done

#python clusterRelated.py
# python updateIndex.py

echo "finished cron activity at $now" > /var/crawlers/article_crawler/logs




