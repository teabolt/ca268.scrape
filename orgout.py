#!/usr/bin/env python3

"""Organise the JSONLines output of the scaper, categorising items under directories/folders and creating .py files for code, based only on the input lines and independent of file organisation, etc"""

import sys
import os
import os.path
import json
import heapq

import utils


class Ca268Organiser(object):
    
    def __init__(self, input_dir, output_dir):
        self.dir_in = input_dir
        self.dir_out = output_dir

        # silently continue if the output directory is present
        os.makedirs(output_dir, exist_ok=True) 

        # a priority queue heap to sort the sections by ID (holds all section data on a live object)
        self.section_heap = []

        # a cross-reference table between section ID and its computerised name
        self.section_index = {}

        # VPL's that are still looking for a section
        self.awaiting_vpls = []

    def _add_section(self, section):
        """Add a section to the index and heap"""
        self.section_index[section['section_id']] = utils.computerise_string(section['section_title'])
        heapq.heappush(self.section_heap, (int(section['section_id']), section))

    def _write_sections(self):
        """Write a summary file for each section found in the section heap, in order"""
        with open(os.path.join(self.dir_out, 'section_descriptors.txt'), 'w') as fsect:
            while self.section_heap:
                section = heapq.heappop(self.section_heap)[1]
                fsect.write(('='*10)+'\n')
                fsect.write('Title: {}\n'.format(section['section_title']))
                if section['section_summary']:
                    fsect.write('Summary: {}\n'.format(section['section_summary']))
                else:
                    fsect.write('Summary: No summary available :-(\n')
                fsect.write('\n\n')

    def _write_section_vpl(self, vpl):
        """Write a VPL under the section it belongs to"""
        if vpl['vpl_section_id'] not in self.section_index:
            raise KeyError('"{}" does not have an associated section in the index'.format(vpl))
        section_dir = os.path.join(self.dir_out, self.section_index[vpl['vpl_section_id']])
        self._write_vpl(vpl, section_dir)

    def _write_vpl(self, vpl, directory):
        """Create a .py and a .txt file for a VPL"""
        if not os.path.isdir(directory):
            os.mkdir(directory)
        computerised_vpl_name = self.computerise_string(vpl['vpl_title'])
        with open(os.path.join(directory, '{}.txt'.format(computerised_vpl_name)), 'w') as finfo:
            if vpl['vpl_code']:
                with open(os.path.join(directory, '{}.py'.format(computerised_vpl_name)), 'w') as fpy:
                    fpy.write(vpl['vpl_code'])
            finfo.write('Title: {}\n'.format(vpl['vpl_title']))
            finfo.write('Description: {}\n'.format(vpl['vpl_description']))
            if vpl['vpl_tests']:
                finfo.write('Tests: {}\n'.format(vpl['vpl_tests']))
            else:
                finfo.write('Tests: No tests available\n')
            if vpl['vpl_grade']:
                finfo.write('Grade: {}\n'.format(vpl['vpl_grade']))
            else:
                finfo.write('Grade: No grade available\n')

    def organise(self):
        """The core method of the class. Orchestrates the organisation of the input"""
        for input_file in os.listdir(self.dir_in):
            with open(os.path.join(self.dir_in, input_file), 'rb') as jsonlines:
                for line in jsonlines:
                    item = json.loads(line)
                    if item['type'] == 'section':
                        self._add_section(item)
                    elif item['type'] == 'vpl':
                        try:
                            self._write_section_vpl(item)
                        except KeyError:
                            awaiting_vpls.append(item)
        self._write_sections()  # process the overall section description
        for vpl in self.awaiting_vpls:
            try:    # check again that section index was not added later
                self._write_section_vpl(vpl)
            except KeyError: 
                other_dir = os.path.join(self.dir_out, 'other')
                self._write_vpl(vpl, other_dir)


def main():
    if not sys.argv[1:]:
        # no arguments
        sys.exit('{} <path_to_input_directory> [path_to_output_directory]'.
            format(os.path.basename(sys.argv[0])))

    # input directory
    input_directory = os.path.abspath(sys.argv[1])
    if not os.path.isdir(input_directory):
        sys.exit('"{}" is not a directory'.format(input_directory))

    # output directory
    if sys.argv[2:]:
        output_directory = sys.argv[2]
    else:
        output_directory = '{}_organised'.format(input_directory)
    output_directory = os.path.abspath(output_directory)

    print('Writing from "{}" to "{}"'.format(input_directory, output_directory))
    organiser = Ca268Organiser(input_directory, output_directory)
    organiser.organise()


if __name__ == '__main__':
    main()