#!/usr/bin/env python3

import subprocess
from os.path import expanduser

basic = ['dialog', '--checklist', 'Choose Vim Settings:', '0', '0', '0']
opt_file = open('options')
opts = []
for line in opt_file:
    opts.append([str.strip(line.split(' ', 1)[0]), str.strip(line.split(' ', 1)[1])])
i = 1
for opt in opts:
    basic += [str(i), opt[1], 'on']
    i += 1
#print(command)
process = subprocess.Popen(basic, stderr=subprocess.PIPE)

results = process.communicate()[1].decode().split()
#print(result)

vimrc = open(expanduser("~")+'/.vimrc', 'w')
for i in range(len(opts)+1)[1:]:
    if str(i) in results:
        print('set', opts[i-1][0], file=vimrc)
    else:
        print('set', 'no' + opts[i-1][0], file=vimrc)

