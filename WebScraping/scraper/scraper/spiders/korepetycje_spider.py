import scrapy
from scrapy.loader import ItemLoader
from scraper.scraper.items import ScraperItem


class KorepetycjeSpider(scrapy.Spider):
    name = "korepetycje"

    def __init__(self, urls, depth=1):
        super(KorepetycjeSpider, self).__init__()
        self.start_urls = urls
        self.depth = depth
        if (self.depth):
            self.counters = dict.fromkeys(self.start_urls, 0)

    def parse(self, response):
        links = response.css(
            "div.main-content a.cat-link-item::attr(href)").getall()
        for link in links:
            yield response.follow(link, callback=self.parse_concrete)

        if (self.depth):
            x = response.url
            url = x if x.find('?strona') == -1 else x[:x.find('?strona')]
            self.counters[url] += 1

            if self.counters[url] < self.depth:
                yield from response.follow_all(css='a[rel="next"]', callback=self.parse)

    def parse_concrete(self, response):
        loader = ItemLoader(item=ScraperItem(), selector=response)
        loader.add_value('link', response.url)
        loaded_name = response.css(
            "div.user-avatar-name-inner::text").getall()[1].split(",")[0].strip()
        loader.add_value('name', loaded_name)
        location, subject = response.css(
            "div.ad-data-col div.ad-data-row span.ad-data-level-name a::text").getall()
        loader.add_value('locations', location.strip())
        loader.add_value('subject', subject.strip())
        loader.add_css('subject', 'div.offermainlisting_item-no strong::text')
        loaded_cost = response.css(
            "div.ad-data-col div.ad-data-row span.ad-data-level-name::text").get()
        loader.add_value('minPrice', self.parse_cost(loaded_cost))
        loader.add_value('maxPrice', self.parse_cost(loaded_cost))
        description = response.css(
            "div.noticeFormWrapper__notice p::text").get()
        loader.add_value('description', self.parse_description(description))
        loader.add_value('origin', 'KOREPETYCJE')
        yield loader.load_item()

    def parse_cost(self, cost):
        return int(cost.strip().split()[0])

    def parse_description(self, loaded_description):
        return loaded_description.strip()
