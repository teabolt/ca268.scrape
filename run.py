#!/usr/bin/env python3

"""
Replacement for using 'scrapy crawl ...' on the command line

Usage:
run.py <course-code> <save-path>
"""

import sys
import os.path

from scrapy.crawler import CrawlerProcess

from poodle_scrp import PoodlerSpider
from poodle_scrp import utils


def main():
    if len(sys.argv) == 3:
        course = sys.argv[1]
        save_dir = sys.argv[2]
    elif len(sys.argv) == 2:
        course = sys.argv[1]
        save_dir = utils.current_datetime()
    else:
        print('Usage:\n\trun.py <course-code> <save-path>')
        raise SystemExit
    save_dir = os.path.abspath(save_dir)

    process = CrawlerProcess()
    process.crawl(PoodlerSpider, course=course, save_dir=save_dir)
    process.start()


if __name__ == '__main__':
    main()