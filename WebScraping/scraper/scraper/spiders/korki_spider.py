import scrapy
from scrapy.loader import ItemLoader
from scraper.scraper.items import ScraperItem


class EKorepetycjeSpider(scrapy.Spider):
    name = "e_korepetycje"

    def __init__(self, urls, depth = 0):
        super(EKorepetycjeSpider, self).__init__()
        self.start_urls = urls
        self.depth = depth
        if(self.depth):
            self.counters = dict.fromkeys(self.start_urls, 0)
    
    def parse(self, response):
        for offer in response.css('div.offer-content'):
            loader = ItemLoader(item=ScraperItem(), selector=offer)
            loader.add_css('name', 'div.offer-large-left h3 a::text')
            loader.add_css('subject', 'span.subject::text')
            loader.add_css('locations', 'span.offer-location::attr(data-original-title)')
            minPrice, maxPrice = self.parse_cost(offer.css('span.cost'))
            loader.add_value('minPrice', minPrice)
            loader.add_value('maxPrice', maxPrice)
            loader.add_xpath('description', 'div[@class="offer-large-left"]/p/span[@itemprop="description"]/text()')
            loader.add_css('link', 'div.offer-large-left h3 a::attr(href)')
            yield loader.load_item()            

        if(self.depth):
            x = response.url
            url = x if x.find('?p') == -1 else x[:x.find('?p')]
            self.counters[url] += 1

            if self.counters[url] < self.depth:
                yield from response.follow_all(css='a.pagination-next', callback=self.parse)
            
            
    
    def parse_cost(self, cost):
        priceContainer = cost.xpath('span[@itemprop="offers"]/span[@itemprop="priceSpecification"]')
        
        if priceContainer.get() is None:
            minPrice = cost.xpath('span[@itemprop="offers"]/span[@itemprop="price"]/text()').get()
            maxPrice = minPrice
        else:
            minPrice = priceContainer.xpath('span[@itemprop="price minPrice"]/text()').get()
            maxPrice = priceContainer.xpath('span[@itemprop="maxPrice"]/text()').get() 

        #returning None if price is not specified (for instance to negotiate)
        return minPrice, maxPrice
    
