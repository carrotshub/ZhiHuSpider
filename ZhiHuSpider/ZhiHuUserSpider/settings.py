# -*- coding: utf-8 -*-

# Scrapy settings for ZhiHuUserSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ZhiHuUserSpider'

SPIDER_MODULES = ['ZhiHuUserSpider.spiders']
NEWSPIDER_MODULE = 'ZhiHuUserSpider.spiders'
TOPIC='人工智能'
# headers
ZHIHU_HEADER = {
    'Host': 'www.zhihu.com',
    'Referer':'https://www.zhihu.com',
    'Connection':'keep-alive',
    'x-udid':'*********************',#在浏览器中获取x_udid的值
    'User-Agent':  'Mozilla/5.0 (Windows NT 10.0; rv:53.0) Gecko/20100101 Firefox/53.0'
}
# cookie,把浏览器里抓取到的cookie填写到这里
ZHIHU_COOKIE = {
    'q_c1': '××××××××××××××××××××××××',
    'd_c0': '×××××××××××××××××××××××',
    '_xsrf': '××××××××××××××××××××××',
    'capsion_ticket': '×××××××××××××××××××××××',
    '_zap': '×××××××××××××××××××××××',
    'tgw_l7_route': '×××××××××××××××××××××',
    'z_c0': '××××××××××××××××××××××××××××××××'
}
#api host headers	
# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'ZhiHuUserSpider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False
#COOKIES_DEBUG=True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}
DOWNLOAD_DELAY=1.5

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'ZhiHuUserSpider.middlewares.MyCustomSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'ZhiHuUserSpider.middlewares.MyCustomDownloaderMiddleware': 543,
   # 'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
   # 'project_name.middlewares.ProxyMiddleware': 100,
   #'scrapy.contrib.downloadermiddlewares.useragent.UserAgentMiddleware':None,
    'scrapy.extensions.downloadermiddlewares.useragent.UserAgentMiddleware':None,
    'ZhiHuUserSpider.middlewares.RotateUserAgentMiddleware':543,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }
#Configure your mysql
MYSQL_HOST='localhost'
MYSQL_USER='username'
MYSQL_PASSWORD='your password'
MYSQL_DB='zhihu'
CHARSET='utf8'
MYSQL_PORT=3306
# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
#   'ZhiHuUserSpider.pipelines.AnsDataCleaning':300,
#   'ZhiHuUserSpider.pipelines.AnsCommCleaning':400,
   'ZhiHuUserSpider.pipelines.ZhihuuserspiderPipeline': 601,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# 设置爬虫的延迟,防止服务器封锁IP
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 80
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
#HTTPERROR_ALLOWED_CODES = []
