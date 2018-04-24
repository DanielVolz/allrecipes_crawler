import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from lxml import html

class Scrapy1Spider(CrawlSpider):
    name = "craiglist"
    allowed_domains = ["sfbay.craigslist.org"]
    start_urls = (
        'http://sfbay.craigslist.org/search/npo',
    )

    rules = (Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@class="button next"]',)), callback="parse_page", follow= True),)

    def parse_page(self, response):
        print(response.url)
        # site = html.fromstring(response.body_as_unicode())
        # titles = site.xpath('//div[@class="content"]/p[@class="row"]')
        # print len(titles), 'AAAA'
