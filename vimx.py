#!/usr/bin/env python3

import subprocess
from os.path import expanduser

command = ['dialog', '--checklist', 'Choose Vim Settings:', '0', '0', '0']
opt_file = open('options')
opts = []
for line in opt_file:
    opts.append([str.strip(line.split(' ', 1)[0]), str.strip(line.split(' ', 1)[1])])
i = 1
for opt in opts:
    command += [str(i), opt[1], 'on']
    i += 1
#print(command)
process = subprocess.Popen(command, stderr=subprocess.PIPE)

results = process.communicate()[1].decode().split()
#print(result)

vimrc = open(expanduser("~")+'/.vimrc', 'w')
for result in results:
    print('set', opts[eval(result)-1][0], file=vimrc)



