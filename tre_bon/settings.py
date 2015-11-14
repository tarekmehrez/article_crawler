# -*- coding: utf-8 -*-

# Scrapy settings for tre_bon project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'tre_bon'

SPIDER_MODULES = ['tre_bon.spiders']
NEWSPIDER_MODULE = 'tre_bon.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tre_bon (+http://www.yourdomain.com)'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS=1

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY=3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN=16
#CONCURRENT_REQUESTS_PER_IP=16

# Disable cookies (enabled by default)
# COOKIES_ENABLED=False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED=False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'tre_bon.middlewares.MyCustomSpiderMiddleware': 543,
#}
DOWNLOADER_MIDDLEWARES = {
    'tre_bon.middlewares.ProxyMiddleware': 110,
    'tre_bon.middlewares.RandomUserAgentMiddleware': 400
} 

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'tre_bon.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
	 'tre_bon.pipelines.ArticlePipeline': 300,
	 'tre_bon.pipelines.VideoPipeline': 300,
	 'tre_bon.pipelines.DuplicatesPipeline': 400,
	 'tre_bon.pipelines.MySQLArticlesPipeline': 500,
	 #'tre_bon.pipelines.MongoArticlesPipeline': 500
}

# ITEM_PIPELINES = {'tre_bon.pipelines.MongoDBPipeline': 300}

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "tre_bon"
MONGODB_COLLECTION = "feed_items"

MYSQLDB_SERVER = "localhost"
MYSQLDB_DB = "threebont"
MYSQLDB_USER = "root"
MYSQLDB_PWD = ""

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
#AUTOTHROTTLE_ENABLED=True
# The initial download delay
#AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED=True
#HTTPCACHE_EXPIRATION_SECS=0
#HTTPCACHE_DIR='httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES=[]
#HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'

PROXIES = [{'ip_port': '61.38.252.17:3128', 'user_pass': ''},
           {'ip_port': '31.15.48.12:80', 'user_pass': ''},
           {'ip_port': '23.239.11.178:56220', 'user_pass': ''},
           {'ip_port': '180.73.0.95:81', 'user_pass': ''},
           {'ip_port': '198.233.177.90:80', 'user_pass': ''},
           {'ip_port': '192.99.198.229:80', 'user_pass': ''},
           {'ip_port': '119.235.102.81:80', 'user_pass': ''},
            {'ip_port': '41.227.136.212:80', 'user_pass': ''},
             {'ip_port': '217.23.185.106:8080', 'user_pass': ''},]

USER_AGENT_LIST = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.152 Safari/535.19',
                   'Mozilla/5.0 (Windows NT 6.1; rv:12.0) Gecko/20120403211507 Firefox/12.0',
                   'Mozilla/5.0 (compatible; Windows; U; Windows NT 6.2; WOW64; en-US; rv:12.0) Gecko/20120403211507 Firefox/12.0']






