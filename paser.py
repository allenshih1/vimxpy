#! /usr/bin/env python3
import os
import json

# vimrc_to_list
def settingFilter(fVimrc):
  configs = []
  for line in fVimrc:
    eachline = line.rstrip().split('\"')
    config = eachline[0].rstrip().split()
    if config:
      configs.append(config)
  return configs

# --------------------------------------------
# Vimrc_paser
# Usage: setting = vimrcPaser(file)
# Input: vimrc file
# Output: setting dict
# --------------------------------------------
def vimrcPaser (fVimrc):
  configs = settingFilter(fVimrc)
  set_Formats = []
  for config in configs:
    # set format
    if ( len(config) == 2 and config[0] == 'set'):
      if ( '=' in config[1]):                                             # with value
        value_assgin_format = config[1].split('=')
        bufDict = { "value":value_assgin_format[0], \
                    "type": "withContent", \
                    "content":value_assgin_format[1]}
        set_Formats.append(bufDict)
      else:                                                               # without value
        bufDict = { "value":config[1], \
                    "type": "onoff", \
                    "content":None}
        set_Formats.append(bufDict)
  return set_Formats


# Example
#vimrcPath = os.path.expanduser("~/.vimrc2")
#fVimrc = open( vimrcPath, "r")
#set_Formats = vimrcPaser(fVimrc)
#for set_Format in set_Formats:
  #print (set_Format)