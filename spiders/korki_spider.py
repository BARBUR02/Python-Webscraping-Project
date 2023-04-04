import scrapy

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
            yield {
                'name': offer.css("div.offer-large-left h3 a::text").get(),
                'subject': offer.css("span.subject::text").get(),
                'locations': offer.css("span.offer-location::attr(data-original-title)").get(),
                'cost': self.parse_cost(offer.css('span.cost')),
                'description': offer.xpath('div[@class="offer-large-left"]/p/span[@itemprop="description"]/text()').get(),
                'link': offer.css("div.offer-large-left h3 a::attr(href)").get(),
            }

        if(self.depth):
            x = response.url
            url = x if x.find('/page') == -1 else x[:x.find('/page')]
            self.counters[url] += 1

            if self.counters[url] < 3:
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
        return (minPrice, maxPrice)
    
