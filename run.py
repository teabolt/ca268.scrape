#!/usr/bin/env python3

"""
Replacement for using 'scrapy crawl ...' on the command line
"""
__use__ = """Usage: `run.py <course-code> [save-dir]`
            'course-code': course to web scrape, one of {ca268, ca269}
            'save-dir': path to the directory where to save, defaults to the current datetime"""
__doc__ += __use__

import sys
import os.path

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

import utils


def main():
    if len(sys.argv) == 3:
        course = sys.argv[1]
        save_dir = sys.argv[2]
    elif len(sys.argv) == 2:
        course = sys.argv[1]
        save_dir = utils.current_datetime()
    else:
        sys.exit(__use__)
    save_dir = os.path.abspath(save_dir)

    process = CrawlerProcess(get_project_settings())
    process.crawl('poodler', course=course, save_dir=save_dir)
    process.start()


if __name__ == '__main__':
    main()