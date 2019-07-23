# -*- coding: utf-8 -*-

import os
import sys

BRANCH = '├───'
END_BRANCH = '└───' 
LEVEL_BRANCH = '│   '

"""
    Format: 
        python dir_struct.py [path [output_path]]

    path:
        Input path. (Default: ".")

    output_path:
        Output path. (Default: ".\\output.txt")
"""

path = '.'
SPLIT = '\\'
dir_path = 'output.txt'
for i in sys.argv[1].split(SPLIT)[::-1]:
    if i != '':
        dir_path = i + '.txt'
        break
output_path = SPLIT.join([path, dir_path])

# Extract parameters.
if len(sys.argv) == 3:
    path = sys.argv[1]
    output_path = sys.argv[2]
elif len(sys.argv) == 2:
    path = sys.argv[1]
elif len(sys.argv) == 1:
    pass

def print_dir(index, root, dir, output):
    cur_dir = root + SPLIT + dir
    
    cur_files = os.listdir(cur_dir)

    output.write(LEVEL_BRANCH * (index - 1) + BRANCH + ' ' + dir + SPLIT + '\n')
    count = 0
    for file in cur_files:
        count += 1
        if not os.path.isdir(SPLIT.join([cur_dir, file])):
            if count == len(cur_files):
                branch = END_BRANCH
            else:
                branch = BRANCH
            output.write(LEVEL_BRANCH * index + branch + ' ' + file + '\n')
        else:
            print_dir(index + 1, cur_dir, file, output)

root_files = os.listdir(path)
start_index = 0
count = 0

with open(output_path, 'w', encoding="utf-8") as output:
    # print(path)
    output.write(path + '\n')
    for root_file in root_files:
        count += 1
        if not os.path.isdir(SPLIT.join([path, root_file])):
            # print(BRANCH, root_file)
            if count == len(root_files):
                branch = END_BRANCH
            else:
                branch = BRANCH
            output.write(branch + ' ' + root_file + '\n')
        else:
            print_dir(start_index + 1, path, root_file, output)
