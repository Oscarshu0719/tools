# -*- coding: utf-8 -*-

import re
import sys


"""
    Usage: 
        python markdown_toc_gen.py path

    Args:
        path: Input path.

    Notice:
        None.
"""

output_path = '.\\toc.txt'
HEADING_PATTERN = r'\s*(#+)\s+(.*)'
TAB = '    '

pattern = re.compile(HEADING_PATTERN)

toc = ''

assert len(sys.argv) == 2, 'Please input the file path.'

with open(sys.argv[1], 'r', encoding='utf8') as input_file:
    for line in input_file:
        match = pattern.match(line)
        if match:
            level = match.group(1).count('#') - 1
            toc += '{}[{}]({}{})\n'.format(level * TAB, match.group(2), 
                match.group(1), match.group(2))

with open(output_path, 'w', encoding='utf8') as output_file:
    output_file.write(toc)
