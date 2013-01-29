# Scrapy settings for soe_crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'soe_crawler'

SPIDER_MODULES = ['soe_crawler.spiders']
NEWSPIDER_MODULE = 'soe_crawler.spiders'

ITEM_PIPELINES = ['soe_crawler.pipelines.SoeCrawlerPipeline',]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'soe_crawler (+http://www.yourdomain.com)'
