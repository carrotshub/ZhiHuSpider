# -*- coding: utf-8 -*-

# Scrapy settings for UserInfo project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'UserInfo'

SPIDER_MODULES = ['UserInfo.spiders']
NEWSPIDER_MODULE = 'UserInfo.spiders'

# headers
ZHIHU_HEADER = {
    'Host': 'www.zhihu.com',
    'Referer':'https://www.zhihu.com',
    'Connection':'keep-alive',
    'x-udid':'ANCmupaVBA6PTnDHURJaEvzrjiBO47cKpvo=',
    'User-Agent':  'Mozilla/5.0 (Windows NT 10.0; rv:53.0) Gecko/20100101 Firefox/53.0'
}
ZHIHU_HEADER_API = {
    'Host': 'api.zhihu.com',
    'Referer':'https://www.zhihu.com',
    'Connection':'keep-alive',
    'x-udid':'ANCmupaVBA6PTnDHURJaEvzrjiBO47cKpvo=',
    'User-Agent':  'Mozilla/5.0 (Windows NT 10.0; rv:53.0) Gecko/20100101 Firefox/53.0'
}
# cookie,把浏览器里抓取到的cookie填写到这里
ZHIHU_COOKIE = {
    'q_c1': '9e7cbcdfb46741e2b739c1b36e945896|1533605922000|1533605922000',
    'd_c0': 'ANCmupaVBA6PTnDHURJaEvzrjiBO47cKpvo=|1533605817',
    '_xsrf': 'sLofnnlZ6etXhDtuaPLDj0WC0KeSflnW',
    'capsion_ticket': '2|1:0|10:1534900981|14:capsion_ticket|44:Y2JhZjg3N2U2NWQ2NDBjYzhmNTVmZTlkNTFjZDZlMzg=|583fe93205424782e58cbbae981c1d1533eb1aaaab7bf0f9f0e398d7e7380a0a',
    '_zap': '09d827af-0234-4142-9bfc-913f7515d537',
    'tgw_l7_route': '200d77f3369d188920b797ddf09ec8d1',
    'z_c0': '2|1:0|10:1534901014|4:z_c0|92:Mi4xNlR2UEF3QUFBQUFBMEthNmxwVUVEaVlBQUFCZ0FsVk5GZ2xxWEFCNHU3QmF5cDVpTnFVTTdMemdoaUN5cTZRUkpn|79d626823ca5465043d77a6552a209360dc65e128d71d8872a4c5673e97d628b'
}


MY_USER_AGENT = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'UserInfo (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

#Configure your mysql
MYSQL_HOST='localhost'
MYSQL_USER='root'
MYSQL_PASSWORD='123456'
MYSQL_DB='zhihu'
CHARSET='utf8'
MYSQL_PORT=3306
# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'UserInfo.middlewares.UserinfoSpiderMiddleware': 543,
#}
DOWNLOADER_MIDDLEWARES ={
        'scrapy.extensions.downloadermiddlewares.useragent.UserAgentMiddleware':None,
        'UserInfo.middlewares.MyUserAgentMiddleware':543
        }
# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'UserInfo.middlewares.UserinfoDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'UserInfo.pipelines.UserinfoPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
