# -*- coding: utf-8 -*-

# Scrapy settings for tre_bon project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

from proxy_list import *
from user_agents import *

BOT_NAME = 'tre_bon'

SPIDER_MODULES = ['tre_bon.spiders']
NEWSPIDER_MODULE = 'tre_bon.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tre_bon (+http://www.yourdomain.com)' , 'user_pass': ''},

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
COOKIES_ENABLED=False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED=False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',\
#   'Accept-Language': 'en',\
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'tre_bon.middlewares.MyCustomSpiderMiddleware': 543,
#}
DOWNLOADER_MIDDLEWARES = {
    # 'tre_bon.middlewares.ProxyMiddleware': 110,
    # 'tre_bon.middlewares.RandomUserAgentMiddleware': 400,

    # 'tre_bon.middlewares.RotateUserAgentMiddleware': 100
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
	'tre_bon.pipelines.MyImagesPipeline':200,
	'tre_bon.pipelines.ArticlePipeline': 300,
	'tre_bon.pipelines.VideoPipeline': 300,
	'tre_bon.pipelines.DuplicatesPipeline': 400,
	'tre_bon.pipelines.MySQLArticlesPipeline': 500,
	 #'tre_bon.pipelines.MongoArticlesPipeline': 500
}

IMAGES_STORE = 'spiders'

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
#HTTPCACHE_DIR='httpcache' , 'user_pass': ''},
#HTTPCACHE_IGNORE_HTTP_CODES=[]
#HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage' , 'user_pass': ''},

PROXIES = proxy_list
USER_AGENT_CHOICES = user_agents


