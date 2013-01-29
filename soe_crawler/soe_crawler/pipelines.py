# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
import csv
from items import SoeCrawlerItem 
class SoeCrawlerPipeline(object):
    def __init__(self):
        self.csv = csv.DictWriter(open('dump.csv', 'wb'), fieldnames=SoeCrawlerItem.fields.keys())
        self.csv.writeheader()

    def process_item(self, item, spider):
        self.csv.writerow(dict(item))
        return item
