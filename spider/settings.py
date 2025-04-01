BOT_NAME = 'name_spider'

SPIDER_MODULES = ['spider.spiders']
NEWSPIDER_MODULE = 'spider.spiders'

ROBOTSTXT_OBEY = True

# Output scraped data to CSV in the project root
FEED_FORMAT = 'csv'
FEED_URI = '../../scraped_data.csv'
