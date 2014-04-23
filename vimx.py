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

def numeric_settings():
    opt_file = open('numeric')
    opts = []
    for line in opt_file:
        linesplit = str.strip(line).split(' ', 2)
        opts.append(linesplit)
    while True:
        numeric = ['dialog', '--menu', 'Numeric', '0', '0', '0']

            
        for opt in opts:
            numeric += [opt[0]+'='+opt[1], opt[2]]

        numeric += ['quit', 'leave the program and save']

        process = subprocess.Popen(numeric, stderr=subprocess.PIPE)
        result = process.communicate()[1].decode()
        if(process.returncode != 0):
            return

        if(result == 'quit'):
            break
        
        default = '0'
        for opt in opts:
            if(opt[0]+'='+opt[1] == result):
                default = opt[1]

        inputbox = ['dialog', '--inputbox', result, '0', '0', default]
        
        process = subprocess.Popen(inputbox, stderr=subprocess.PIPE)
        sub_result = process.communicate()[1].decode()
        if(process.returncode != 0):
            return


        for opt in opts:
            if(opt[0]+'='+opt[1] == result):
                opt[1] = sub_result

    final_settings = ''
    for opt in opts:
            final_settings += 'set ' + opt[0] + '=' + opt[1] + '\n'

    return final_settings
    
def menu():
    basic = ''
    numeric = ''
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
        result = process.communicate()[1].decode()
        if(process.returncode != 0):
            exit
        
        if(result == 'basic'):
            basic = basic_settings() 

        elif(result == 'numeric'):
            numeric = numeric_settings() 

        elif(result == 'quit'):
            return basic + numeric;

all = menu()
vimrc = open(expanduser("~")+'/.vimrc', 'w')
print(all, file=vimrc)
