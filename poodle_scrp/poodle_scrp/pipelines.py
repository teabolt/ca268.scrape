# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonLinesItemExporter
import os
import os.path
import datetime


class PoodleScrpPipeline(object):
    def process_item(self, item, spider):
        return item


class DataTypeJsonLinesExporter(object):
    """Save generated dicts into appropriate JSONLines files, in a new directory"""

    def open_spider(self, spider):
        self.exporters = {}
        # curr_t = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        # self.curr_t = curr_t
        # os.mkdir(curr_t)
        save_dir = spider.save_dir
        self.save_dir = save_dir
        os.makedirs(save_dir, exist_ok=True)

    def close_spider(self, spider):
        for exporter in self.exporters.values():
            exporter.finish_exporting()
            exporter.file.close()

    def _section_exporter(self, item):
        """Retrieve an exporter for section metadata"""
        if 'all_sections' not in self.exporters:
            f = open(os.path.join(self.save_dir, 'sections.jsonlines'), 'wb')
            exporter = JsonLinesItemExporter(f)
            self.exporters['all_sections'] = exporter
            exporter.start_exporting()
        return self.exporters['all_sections']            

    def _vpl_exporter(self, item):
        """Retrieve an exporter for a Virtual Programming Lab that belongs to a section"""
        exporter_name = 'vpls_section_{}'.format(item['vpl_section_id'])
        if exporter_name not in self.exporters:
            f = open(os.path.join(self.save_dir, 'vpls{}.jsonlines'.format(item['vpl_section_id'])), 'wb')
            exporter = JsonLinesItemExporter(f)
            self.exporters[exporter_name] = exporter
            exporter.start_exporting()
        return self.exporters[exporter_name]

    def process_item(self, item, spider):
        which = item['type']
        if which == 'section':
            exporter = self._section_exporter(item)
        elif which == 'vpl':
            exporter = self._vpl_exporter(item)
        exporter.export_item(item)
        return item
