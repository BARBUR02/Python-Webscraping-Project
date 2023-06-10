from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.settings import Settings

from twisted.internet import reactor
from scraper.scraper import settings as my_settings
from scraper.scraper.app_settings import E_KOREPETYCJE_URLS, E_KORKI_URLS, KOREPETYCJE_URLS
from scraper.scraper.spiders.korki_spider import EKorepetycjeSpider
from scraper.scraper.spiders.e_korki_spider import EKorkiSpider
from scraper.scraper.spiders.korepetycje_spider import KorepetycjeSpider
from main.models import Offert


class Command(BaseCommand):
    help = 'Release spider'

    def handle(self, *args, **options):
        self.__delete_offerts()

        crawler_settings = Settings()
        crawler_settings.setmodule(my_settings)
        runner = CrawlerRunner(crawler_settings)

        self.__crawl_e_korepetycje(runner)
        self.__crawl_e_korki(runner)
        self.__crawl_korepetycje(runner)

        d = runner.join()
        d.addBoth(lambda _: reactor.stop())
        reactor.run()

    def __crawl(self, process, urls, spider, depth):
        process.crawl(spider, urls=urls, depth=depth)

    def __crawl_e_korepetycje(self, process, jl_file='', depth=2):
        self.__crawl(process, E_KOREPETYCJE_URLS, EKorepetycjeSpider, depth)

    def __crawl_e_korki(self, process, jl_file='', depth=4):
        self.__crawl(process, E_KORKI_URLS, EKorkiSpider, depth)

    def __crawl_korepetycje(self, process, jl_file='', depth=4):
        self.__crawl(process, KOREPETYCJE_URLS, KorepetycjeSpider, depth)

    def __delete_offerts(self):
        Offert.objects.filter(from_our_user=False).delete()
