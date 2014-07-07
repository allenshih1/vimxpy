#! /usr/bin/env python

import parser
import argparse

argParser = argparse.ArgumentParser(description='Vimrc parser')
argParser.add_argument('-i', type=argparse.FileType('r'))
args = argParser.parse_args()
vimrcfile = args.i
options = parser.vimrcParser(vimrcfile, 'set')

for option in options:
  print(option)
