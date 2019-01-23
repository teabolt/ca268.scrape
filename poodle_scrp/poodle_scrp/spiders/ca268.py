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

        for section_link in sections.css('.section-title a')[10:11]:
            section_request = response.follow(
                section_link, 
                callback=self.parse_section,
            )
            section_request.meta['original_section_url'] = section_link.xpath('@href').extract_first()
            yield section_request

    def parse_section(self, response):
        # to identify the main content in the response, need to know the section id
        section_url = response.meta['original_section_url']
        url_qs = urllib.parse.parse_qs(urllib.parse.urlparse(section_url).query)
        section_content = response.css('#section-{} .section'.format(url_qs['section'][0]))
        # section_content = response.css('#section-9 .section')
        vpls = section_content.css('.vpl')
        for vpl in vpls[:3]:
            yield {'vpl_title': vpl.css('::text').extract_first()}

        for vpl_a in vpls.css('a')[:3]:
            yield response.follow(
                vpl_a,
                callback=self.parse_vpl)

    def parse_vpl(self, response):
        main = response.css('.box > .box')
        text = main.css('p, pre').css('::text')
        description = text.extract()
        yield {
            'vpl_description': '\n'.join(description)
        }

        submissionview = response.css('[role="main"] .nav [title="Submission view"]')
        if submissionview:  # if non-empty list
            yield response.follow(submissionview[0], callback=self.parse_submissionview)

    def parse_submissionview(self, response):
        # parsing must happen before JavaScript is ran on the DOM (on the raw HTML sourcecode) (afterards, Ace Editor styles and distributes the code over many elements)
        code = response.css('[role="main"] #codefileid1 ::text') 
        yield {'vpl_code': code.extract_first()}
        # code to get upload / test info ...
