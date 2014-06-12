#! /usr/bin/env python3
import os
import json
import re

# vimrc_to_list
def settingFilter(fVimrc):
  configs = []
  for line in fVimrc:
    eachline = line.rstrip().split('\"')
    config = eachline[0].rstrip().split()
    if config:
      configs.append(config)
  return configs

def isAttr(string):
  attr = ['<buffer>', '<silent>', '<expr>',  '<script>', '<unique>', '<special>']
  return string in attr

def isMap(string):
  return re.search('^[nvxosilc]?(nore)?map(c|clear)?$|^[nvxoilc]?m$|^[nvxl]?n|^no(!)?$|^[oic]?n$|^sonr^|^map(c|clear)?!$', string)

def concatFrom(inList, start):
  string = ''
  for index in range(start, len(inList)):
    if (index == start):
      string = inList[index]
    else:
      string += ' ' + inList[index]
  return string

# --------------------------------------------
# Vimrc_paser
# Usage: setting = vimrcPaser(file)
# Input: vimrc file
# Output: setting dict
# --------------------------------------------
def vimrcPaser (fVimrc, myfilter):
  configs = settingFilter(fVimrc)
  filtered = []
  for config in configs:
    # set format
    if ( myfilter == 'set' and len(config) == 2 and config[0] == 'set'):
      if ( '=' in config[1]):                                             # with value
        value_assgin_format = config[1].split('=')
        bufDict = { "value"   : value_assgin_format[0], \
                    "type"    : "withContent",          \
                    "content" : value_assgin_format[1]}
        filtered.append(bufDict)
      else:                                                               # without value
        bufDict = { "value"   : config[1], \
                    "type"    : "onoff",   \
                    "content" : None}
        filtered.append(bufDict)
    elif (myfilter == 'map' and isMap(config[0]) ):
      if (len(config) == 3):
        bufDict = { "type"      : config[0], \
                    "attr"     : None,      \
                    "key"      : config[1], \
                    "command"  : concatFrom(config, 2)
                  }
      elif (len(config) >= 3):
        if (isAttr( config[1]) ):
          bufDict = { "type"      : config[0], \
                      "attr"     : config[1], \
                      "key"      : config[2], \
                      "command"  : concatFrom(config, 3)
                    }
        else:
          bufDict = { "type"      : config[0], \
                      "attr"     : None,      \
                      "key"      : config[1], \
                      "command"  : concatFrom(config, 2)
                    }
      filtered.append(bufDict)
  return filtered


# Example
#vimrcPath = os.path.expanduser("~/.vimrc2")
#fVimrc = open( vimrcPath, "r")
#set_Formats = vimrcPaser(fVimrc, 'map')
#for set_Format in set_Formats:
  #print (set_Format)
