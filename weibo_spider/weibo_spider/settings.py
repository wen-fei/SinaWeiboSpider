# -*- coding: utf-8 -*-

# 爬虫基本属性
BOT_NAME = 'weibo_spider'
SPIDER_MODULES = ['weibo_spider.spiders']
NEWSPIDER_MODULE = 'weibo_spider.spiders'

LOG_LEVEL = 'INFO'    # 日志级别
LOG_FILE = 'weiboSpider.log'  # 存在该设置则输出到该文件中，否则输出至标准错误输出

# 大V
bigV = [
    1826792401, 3937348351, 5548590926, 1896891963,
    1323527941, 1618051664, 1326410461, 2607072084, 2108172317,
]


# 微博账号密码
myWeiBo = [
    ('17722173610', 'qsy9tugw '),
    ('17722177843', 'k2pccrfd '),
    ('17722176697', '1mqinzch '),
    ('17722179551', '8ccldtib '),
    ('17722179884', 'vay0xhsif '),
    ('17722177707', 'b4oamnmr '),
    ('bajiao26341950@163.com', 'tttt5555'),
    ('pinjian80@163.com', 'tttt5555'),
    ('huangzhimeifent@163.com', 'tttt5555'),
    ('pintuo17339719@163.com', 'tttt5555'),
    ('weizongchensipu@163.com', 'tttt5555'),
    ('liaogua68@163.com', 'tttt5555'),
    ('15164279524', 'Q474312827'),
    ('17131031514', 'Q474312827'),
    ('18445714564', 'Q474312827'),
]
# Mongodb绑定
MONGO_URI = 'mongodb://localhost:27017/'
MONGO_DATABASE = 'SinaWeibo2'

# Redis Cookie 存储，方便JOB暂停开启
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

# 爬虫中间件注册
DOWNLOADER_MIDDLEWARES = {
    "weibo_spider.middlewares.UserAgentMiddleware": 401,
    "weibo_spider.middlewares.CookiesMiddleware": 402,
}


# 爬虫管道注册
ITEM_PIPELINES = {
    'weibo_spider.pipelines.MongoDBPipeline': 300,
}


# 注释掉，改为深度优先
# 最大深度为3，广度优先。
# DEPTH_PRIORITY = 3
# SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleFifoDiskQueue'
# SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.FifoMemoryQueue'


# 页面下载时间间隔  3秒间隔
DOWNLOAD_DELAY = 3

# 是否跳转至新页面
REDIRECT_ENABLED = False

# CONCURRENT_ITEMS = 1000
# CONCURRENT_REQUESTS = 100
# REDIRECT_ENABLED = False
# CONCURRENT_REQUESTS_PER_DOMAIN = 100
# CONCURRENT_REQUESTS_PER_IP = 0
# CONCURRENT_REQUESTS_PER_SPIDER=100
# DNSCACHE_ENABLED = True
# CONCURRENT_REQUESTS = 70


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
#    'weibo_spider.middlewares.WeiboSpiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'weibo_spider.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'weibo_spider.pipelines.SomePipeline': 300,
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
