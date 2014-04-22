#!/usr/bin/env python3

import subprocess
from os.path import expanduser

def basic_settings():
    basic = ['dialog', '--checklist', 'Choose Vim Settings:', '0', '0', '0']
    opt_file = open('options')
    opts = []

    for line in opt_file:
        linesplit = str.strip(line).split(' ', 2)
        opts.append(linesplit)
        
    for opt in opts:
        basic += [opt[0], opt[2], opt[1]]

    process = subprocess.Popen(basic, stderr=subprocess.PIPE)
    results = process.communicate()[1].decode().split()
    
    final_settings = ''
    for opt in opts:
        if opt[0] in results:
            final_settings += 'set ' + opt[0] + '\n'
        else:
            final_settings += 'set no' + opt[0] + '\n'

    return final_settings
    
def menu():
    basic = ''
    while True:
        menu = ['dialog', '--menu', 'VIMX', '0', '0', '0']
        menu_file = open('menu')
        opts = []
        
        for line in menu_file:
            linesplit = str.strip(line).split(' ', 1)
            opts.append(linesplit)
        
        for opt in opts:
            menu += [opt[0], opt[1]]
        menu += ['quit', 'leave the program and save']
            
        process = subprocess.Popen(menu, stderr=subprocess.PIPE)
        print(process.returncode)
        result = process.communicate()[1].decode()
        if(process.returncode != 0):
            exit
        
        if(result == 'basic'):
            basic = basic_settings() 

        elif(result == 'quit'):
            return basic;

all = menu()
vimrc = open(expanduser("~")+'/.vimrc', 'w')
print(all, file=vimrc)
