from scrapy.crawler import CrawlerProcess
from app_settings import E_KOREPETYCJE_URLS
from spiders.korki_spider import EKorepetycjeSpider

def _crawl(urls, spider, settings, depth):
    process = CrawlerProcess(settings)
    process.crawl(spider, urls = urls, depth = depth)
    process.start()

def crawl_e_korepetycje(jl_file, depth = 3):
    settings = {
        "FEEDS": { jl_file: { "format": "jl" } },
        "FEED_EXPORT_ENCODING": 'utf-8',
        "BOT_NAME": "e_korepetycje",
        "ROBOTSTXT_OBEY": True
    }
    _crawl(E_KOREPETYCJE_URLS, EKorepetycjeSpider, settings, depth)