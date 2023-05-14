from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings


from scraper.scraper import settings as my_settings
from scraper.scraper.app_settings import E_KOREPETYCJE_URLS
from scraper.scraper.spiders.korki_spider import EKorepetycjeSpider
from main.models import Offert

class Command(BaseCommand):
    help = 'Release spider'

    def handle(self, *args, **options):
        self.__delete_offerts()
        self.__crawl_e_korepetycje()

    def __crawl(self, urls, spider, settings, depth):
        crawler_settings = Settings()
        crawler_settings.setmodule(settings)
        process = CrawlerProcess(crawler_settings)
        process.crawl(spider, urls = urls, depth = depth)
        process.start()

    def __crawl_e_korepetycje(self, jl_file='', depth = 2):
        settings = my_settings
        self.__crawl(E_KOREPETYCJE_URLS, EKorepetycjeSpider, settings, 20)

    def __delete_offerts(self):
        Offert.objects.all().delete()