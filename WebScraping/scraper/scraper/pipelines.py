# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from main.models import Offert

class ScraperPipeline(object):
    def process_item(self, item, spider):
        item.save()
        return item

class CostPipeline(object):
    def process_item(self, item, spider):
        if item.get('minPrice'):
            item['minPrice'] = int(item['minPrice'][0]) if item['minPrice'] is not None else None
        if item.get('maxPrice'):
            item['maxPrice'] = int(item['maxPrice'][0]) if item['maxPrice'] is not None else None
        return item
    
class TableErrorPipeline(object):
    def process_item(self, item, spider):
        if item.get('name'):
            item['name'] = item['name'][0]
        if item.get('subject'):
            item['subject'] = item['subject'][0].capitalize()
        if item.get('description'):
            item['description'] = item['description'][0]
        if item.get('locations'):
            item['locations'] = item['locations'][0]
        if item.get('link'):
            item['link'] = item['link'][0]
        if item.get('origin'):
            item['origin'] = item['origin'][0]
        return item