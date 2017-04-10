BOT_NAME = 'music'

SPIDER_MODULES = ['music.spiders']
NEWSPIDER_MODULE = 'music.spiders'

DOWNLOAD_HANDLERS = {'s3': None}

ITEM_PIPELINES = {
    'music.pipelines.MongoDBPipeline': 300,
}

MONGODB_SERVER = "localhost"
MONGODB_PORT = "27017"
MONGODB_DB = "music"
MONGODB_USER = ""
MONGODB_PASS = ""
MONGODB_COLLECTION_MUSIC_NCT = "music_nct"

DOWNLOAD_DELAY = 1
# Retry many times since proxies often fail
RETRY_TIMES = 5

# Retry on most error codes since proxies fail for different reasons
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    'music.randomproxy.RandomProxy': 100,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 120
}

HTTPCACHE_ENABLED = False
HTTPCACHE_EXPIRATION_SECS = 2 * 24 * 60 * 60
HTTPCACHE_GZIP = True

PROXY_LIST = 'music/proxy/proxy-list.txt'
LOG_LEVEL = 'INFO'
