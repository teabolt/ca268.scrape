#!/usr/bin/env python3

"""Execute scrapers from this script instead of using 'scrapy crawl'"""

import sys

from scrapy.crawler import CrawlerProcess




def main():
    process = CrawlerProcess()
    process.crawl('poodler')
    # process.crawl(MySpider2)
    process.start()


if __name__ == '__main__':
    main()