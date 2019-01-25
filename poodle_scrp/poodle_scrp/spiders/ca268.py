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
        # for section in sections:
        #     title = section.css('.section-title a ::text').extract_first()
        #     if title is not None:
        #         title = title.strip()
        #     summary = ' '.join(section.css('.summarytext p ::text').extract()).replace('\r\n', '').strip()
        #     yield {
        #         'section_title': title,
        #         'section_summary': summary,
        #     }

        for section_link in sections.css('.section-title a')[-1:-4:-2]:
            section_request = response.follow(
                section_link, 
                callback=self.parse_section,
            )
            section_request.meta['url_to_section'] = section_link.xpath('@href').extract_first()
            yield section_request

    def parse_section(self, response):
        # need to know the section id in order to identify the main content of the page
        section_url = response.meta['url_to_section']
        # section_url = 'https://poodle.computing.dcu.ie/moodle/course/view.php?id=4&section=4'
        querystring = urllib.parse.parse_qs(urllib.parse.urlparse(section_url).query)
        section_identifier = '#section-{}'.format(querystring['section'][0])
        section_title = response.css('#region-main .navigationtitle .sectionname ::text')
        section_summary = response.css('{} .summary ::text'.format(section_identifier))
        yield {
            'type':'section',
            'section_title': section_title.extract_first(),
            'section_summary': ' '.join(section_summary.extract()).replace('\r\n', '').strip(),
        }

        # for vpl in vpls:
        #     yield {'vpl_title': vpl.css('::text').extract_first()}

        for vpl_a in response.css('{} .vpl a'.format(section_identifier)):
            yield response.follow(
                vpl_a,
                callback=self.parse_vpl)

    def parse_vpl(self, response):
        """Follow links to the Virtual Programming Labs"""
        vpl_title = response.css('[role="main"] > h2::text')
        vpl_body = response.css('.box > .box')
        vpl_description = vpl_body.css('p, pre').css('::text')
        vpl_item = {
            'type': 'vpl',
            'vpl_title': vpl_title.extract_first(),
            'vpl_description': '\n'.join(vpl_description.extract())
        }

        submissionview_link = response.css('[role="main"] .nav [title="Submission view"]')
        if submissionview_link:  # if non-empty list
            submission_request = response.follow(submissionview_link[0], callback=self.parse_submissionview)
            submission_request.meta['vpl_item'] = vpl_item
            yield submission_request

    def parse_submissionview(self, response):
        # parsing must happen before JavaScript is ran on the DOM (on the raw HTML sourcecode) (afterards, Ace Editor styles and distributes the code over many elements)
        vpl_item = response.meta['vpl_item']
        # vpl_item = {
        # 'type':'vpl',
        # 'vpl_title':'How many items',
        # 'vpl_description':'abababa test',
        # }
        code = response.css('[role="main"] #codefileid1 ::text')
        vpl_item['vpl_code'] = code.extract_first()

        assessment = response.css('.box')
        tests = assessment.re_first('[^|]*run[^|]*')
        if tests:
            tests = tests.strip()
        vpl_item['vpl_tests'] = tests

        grade = assessment.xpath('//b[text()="grade"]/following-sibling::text()[1]').re_first('[0-9]+')
        try:
            grade = int(grade)
        except ValueError:
            pass
        vpl_item['vpl_grade'] = grade

        yield vpl_item
