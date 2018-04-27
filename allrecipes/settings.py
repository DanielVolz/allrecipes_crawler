# -*- coding: utf-8 -*-

# Scrapy settings for allrecipes project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'scrapybot'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'
SPIDER_MODULES = ['allrecipes.spiders']
NEWSPIDER_MODULE = 'allrecipes.spiders'

#DOWNLOAD_DELAY = .25
#RANDOMIZE_DOWNLOAD_DELAY = True

DOWNLOAD_DELAY = 2

AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 2
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 6
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = True

DUPEFILTER_CLASS = 'scrapy.dupefilters.BaseDupeFilter'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'allrecipes (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Retry many times since proxies often fail
RETRY_TIMES = 10
# Retry on most error codes since proxies fail for different reasons
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]

# DOWNLOADER_MIDDLEWARES = {
#     'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
#     'scrapy_proxies.RandomProxy': 100,
#     'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
# }

# Proxy list containing entries like
# http://host1:port
# http://username:password@host2:port
# http://host3:port
# ...
PROXY_LIST = 'proxylist.txt'

# Proxy mode
# 0 = Every requests have different proxy
# 1 = Take only one proxy from the list and assign it to every requests
# 2 = Put a custom proxy to use in the settings
PROXY_MODE = 0

# If proxy mode is 2 uncomment this sentence :
#CUSTOM_PROXY = "http://host1:port"

# -----------------------------------------------------------------------------
# SCRAPY HTTPCACHE SETTINGS
# -----------------------------------------------------------------------------
DOWNLOADER_MIDDLEWARES = {
    'scrapy_proxies.RandomProxy': None,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 543,
    'scrapy.downloadermiddlewares.stats.DownloaderStats': 850,
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 900,
}
HTTPCACHE_POLICY = 'scrapy.extensions.httpcache.RFC2616Policy'

# DOWNLOADER_MIDDLEWARES.update({
#     'scrapy_httpcache.downloadermiddlewares.httpcache.AsyncHttpCacheMiddleware': 900,
#
# })

HTTPCACHE_ENABLED = False
HTTPCACHE_IGNORE_HTTP_CODES = [301, 302, 500, 503]
# HTTPCACHE_STORAGE = 'scrapy_httpcache.extensions.httpcache_storage.MongoDBCacheStorage'
# HTTPCACHE_MONGODB_HOST = '127.0.0.1'
# HTTPCACHE_MONGODB_PORT = 27017
# HTTPCACHE_MONGODB_USERNAME = ''
# HTTPCACHE_MONGODB_PASSWORD = ''
# HTTPCACHE_MONGODB_AUTH_DB = ''
# HTTPCACHE_MONGODB_DB = 'cache_storage'
# HTTPCACHE_MONGODB_COLL = 'cache'
#
# # -----------------------------------------------------------------------------
# # SCRAPY HTTPCACHE BANNED SETTINGS (optional)
# # -----------------------------------------------------------------------------
# BANNED_STORAGE = 'scrapy_httpcache.extensions.banned_storage.MongoBannedStorage'
#
# # -----------------------------------------------------------------------------
# # SCRAPY HTTPCACHE REQUEST ERROR SETTINGS (optional)
# # -----------------------------------------------------------------------------
# REQUEST_ERROR_STORAGE = 'scrapy_httpcache.extensions.request_error_storage.MongoRequestErrorStorage'



LOG_FILE = 'scrapy.log'
LOG_STDOUT = True
DUPEFILTER_DEBUG = True

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'allrecipes.pipelines.MongoPipeline': 300,
}
MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'recipe_db'


# COOKIES_DEBUG = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'allrecipes.middlewares.AllrecipesSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'allrecipes.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'allrecipes.pipelines.AllrecipesPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
