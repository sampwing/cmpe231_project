from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from soe_crawler.items import SoeCrawlerItem
from scrapy import log
import re

class SoeSpider(CrawlSpider):
    name = 'soespider'
    start_urls = ['http://courses.soe.ucsc.edu/'] # urls from which the spider will start crawling
    rules = [Rule(SgmlLinkExtractor(allow=[r'courses/\w+\d+\w*?']), callback='parse_course')]
        # r'courses/\w+\d+\w*?' : regular expression for http://isbullsh.it/page/X URLs

    def parse_course(self, response):
        hxs = HtmlXPathSelector(response)
        item = SoeCrawlerItem()
        #item['course_info'] 
        course_info = hxs.select('/html/body/div[2]/div[3]/div/div/h1/text()').extract()[0]
        rx_result = re.search(r'(?P<course_number>\w+\d+\w*?)\s*:\s*(?P<course_name>[a-zA-Z0-9 :&#;,+()-/\']+)', course_info)
        if rx_result:
            item['name'] = rx_result.group('course_name')
            item['number'] = rx_result.group('course_number')
        item['description'] = hxs.select('/html/body/div[2]/div[3]/div/div[3]/p/text()').extract()
        item['fall'] = hxs.select('//tr[@class="odd"][1]/td[2]//a/text()').extract() or ' '
        item['winter'] = hxs.select('//tr[@class="odd"][1]/td[3]//a/text()').extract() or ' '
        item['spring'] = hxs.select('//tr[@class="odd"][1]/td[4]//a/text()').extract() or ' '
        item['summer'] = hxs.select('//tr[@class="odd"][1]/td[5]//a/text()').extract() or ' '
        return item


