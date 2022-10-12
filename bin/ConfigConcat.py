#!/usr/bin/env python3
import sys
import os

from parablade.common.config import ReadUserInput, ConcatenateConfig, WriteBladeConfigFile


DIR = os.getcwd() + '/'
files = sys.argv[1:]

list_to_concat = []
for file in files:
    list_to_concat.append(ReadUserInput(DIR+file))

final = ConcatenateConfig(*list_to_concat)

WriteBladeConfigFile(open(DIR+files[0][:-4]+'_concatenated.cfg', 'w'), final)

print(f'File written to {DIR+files[0][:-4]+"_concatenated.cfg"}')
