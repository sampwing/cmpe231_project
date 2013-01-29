# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class SoeCrawlerItem(Item):
    name = Field()
    number = Field()
    #course_info = Field()
    description = Field()
    fall = Field()
    winter = Field()
    spring = Field()
    summer = Field()

