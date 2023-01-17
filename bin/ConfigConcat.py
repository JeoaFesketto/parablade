#!/usr/bin/env python3
import sys
import os

from parablade.common.config import read_user_input, concatenate_config_files, write_blade_config_file


DIR = os.getcwd() + '/'
files = sys.argv[1:]

list_to_concat = []
for file in files:
    list_to_concat.append(read_user_input(DIR+file))

final = concatenate_config_files(*list_to_concat)
final['NDIM'] = 3

write_blade_config_file(open(DIR+files[0][:-4]+'_concatenated.cfg', 'w'), final)

print(f'File written to {DIR+files[0][:-4]+"_concatenated.cfg"}')
