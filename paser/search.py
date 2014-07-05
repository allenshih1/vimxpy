#! /usr/bin/env python

def searchInVimrc(searchKey, options, searchFeild):
  for option in options:
    if option[searchFeild] == searchKey:
      return option
  else:
    return None
