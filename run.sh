now=$(date +%Y-%m-%d:%H:%M:%S)
for spider in $(scrapy list); do
	echo Running crawler: $spider, saving logs to logs/crawlers-logs/${spider}.${now}.log
	scrapy crawl $spider --logfile logs/crawlers-logs/${spider}.${now}.log -o data/json-data/${spider}.${now}.json
done