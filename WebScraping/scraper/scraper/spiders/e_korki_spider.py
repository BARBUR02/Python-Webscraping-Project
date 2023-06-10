import scrapy
from scrapy.loader import ItemLoader
from scraper.scraper.items import ScraperItem


class EKorkiSpider(scrapy.Spider):
    name = "e_korki"

    def __init__(self, urls, depth=1):
        super(EKorkiSpider, self).__init__()
        self.start_urls = urls
        self.depth = depth
        if (self.depth):
            self.counters = dict.fromkeys(self.start_urls, 0)

    def parse(self, response):
        for offer in response.css('div.certificate_trow'):
            loader = ItemLoader(item=ScraperItem(), selector=offer)
            loader.add_css('name', 'div.offermainlisting_item-subject a::text')
            loader.add_css(
                'subject', 'div.offermainlisting_item-no strong::text')
            location_text = offer.css(
                'div.offermainlisting_item-place a::text')[1].get()
            loader.add_value('locations', self.parse_locations(location_text))
            loaded_price = offer.css('div.pr0::text').get()
            price = self.parse_cost(loaded_price)
            loader.add_value('minPrice', price)
            loader.add_value('maxPrice', price)
            loaded_description = offer.css(
                "div.offermainlisting_item-desc a::text").get()
            loader.add_value(
                'description', self.parse_description(loaded_description))
            loaded_link = offer.css(
                "div.offermainlisting_item-desc a::attr(href)").get()
            loader.add_value('link', self.parse_link(
                "https://ekorki.pl", loaded_link))
            loader.add_value('origin', 'E_KORKI')
            yield loader.load_item()

        if (self.depth):
            x = response.url
            url = x if x.find('?page') == -1 else x[:x.find('?page')]
            self.counters[url] += 1

            if self.counters[url] < self.depth:
                yield from response.follow_all(css='a#next', callback=self.parse)

    def parse_cost(self, cost):
        return int(cost.strip().split()[0])

    def parse_locations(self, scraped_text):
        _, location = scraped_text.strip().split(", ")
        return location

    def parse_description(self, loaded_description):
        return loaded_description.strip()

    def parse_link(self, base_link, link_extension):
        return base_link.strip() + link_extension.strip()
