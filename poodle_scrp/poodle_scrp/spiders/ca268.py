# -*- coding: utf-8 -*-

import scrapy
import getpass
import urllib.parse


class Ca268Spider(scrapy.Spider):
    name = 'ca268'
    allowed_domains = ['poodle.computing.dcu.ie']

    def start_requests(self):
        return [scrapy.Request('https://poodle.computing.dcu.ie/moodle/course/view.php?id=4', callback=self.log_in)]

    def log_in(self, response):
        # some info on 302's https://stackoverflow.com/questions/20805932/scrapy-retry-or-redirect-middleware
        return scrapy.FormRequest.from_response(
            response,
            formid='login',
            formdata={
                'username': input('Username: '), 
                'password': getpass.getpass('Password: ')
                },
            dont_filter=True,
        )

    def parse(self, response):
        sections = response.css('.topics > li')
        for section in sections:
            title = section.css('.section-title a ::text').extract_first()
            if title is not None:
                title = title.strip()
            summary = ' '.join(section.css('.summarytext p ::text').extract()).replace('\r\n', '').strip()
            yield {
                'section_title': title,
                'section_summary': summary,
            }

        for section_link in sections.css('.section-title a'):
            section_request = response.follow(
                section_link, 
                callback=self.parse_section,
            )
            section_request.meta['original_section_url'] = section_link.xpath('@href').extract_first()
            yield section_request

    def parse_section(self, response):
        # to identify the main content, need to know the section id from the request query string
        # need to use META: https://stackoverflow.com/questions/20081024/scrapy-get-request-url-in-parse
        section_url = response.meta['original_section_url']
        url_qs = urllib.parse.parse_qs(urllib.parse.urlparse(section_url).query)
        section_content = response.css('#section-{} .section'.format(url_qs['section'][0]))
        # section_content = response.css('#section-9 .section')
        vpls = section_content.css('.vpl')
        for vpl in vpls:
            yield {'vpl_title': vpl.css('::text').extract_first()}
        # for vpl in vpls:
        #     yield response.follow(
        #         vpl.css('a'),
        #         callback=self.parse_vpl)

    def parse_vpl(self, response):
        main = response.css('.box > .box')
        text = main.css('p, pre').css('::text')
        description = text.extract()
        yield {
            'vpl_description': '\n'.join(description)
        }
        # xpath to find 'a' tag by 'submissionview' text
        # request to it, handler for it

    def parse_submissionview(self, response):
        pass
        # code to get actual source (not scripted by ace editor)