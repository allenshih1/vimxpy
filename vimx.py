#!/usr/bin/env python3

import subprocess
import os

def basic_settings(default_run):
    opt_file = open(os.path.join(os.path.dirname(__file__), 'options'))
    opts = []
    for line in opt_file:
        linesplit = str.strip(line).split(' ', 2)
        opts.append(linesplit)

    if not default_run:
        basic = ['dialog', '--checklist', 'Choose Vim Settings:', '0', '0', '0']

        for line in opt_file:
            linesplit = str.strip(line).split(' ', 2)
            opts.append(linesplit)
            
        for opt in opts:
            basic += [opt[0], opt[2], opt[1]]

        process = subprocess.Popen(basic, stderr=subprocess.PIPE)
        results = process.communicate()[1].decode().split()

        if(process.returncode == 0):
            for opt in opts:
                if opt[0] in results:
                    opt[1] = 'on'
                else:
                    opt[1] = 'off'

    final_settings = ''
    for opt in opts:
        if(opt[1] == 'on'):
            final_settings += 'set ' + opt[0] + '\n'
        else:
            final_settings += 'set no' + opt[0] + '\n'

    return final_settings

def numeric_settings(default_run):
    opt_file = open(os.path.join(os.path.dirname(__file__), 'numeric'))
    opts = []
    for line in opt_file:
        linesplit = str.strip(line).split(' ', 2)
        opts.append(linesplit)
    while not default_run:
        numeric = ['dialog', '--menu', 'Numeric', '0', '0', '0']

            
        for opt in opts:
            numeric += [opt[0]+'='+opt[1], opt[2]]

        numeric += ['quit', 'leave the program and save']

        process = subprocess.Popen(numeric, stderr=subprocess.PIPE)
        result = process.communicate()[1].decode()

        if(process.returncode != 0):
            break

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
    basic = basic_settings(True) 
    numeric = numeric_settings(True) 
    while True:
        menu = ['dialog', '--menu', 'VIMX', '0', '0', '0']
        menu_file = open(os.path.join(os.path.dirname(__file__), 'menu'))
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
            return ''
        
        if(result == 'basic'):
            basic = basic_settings(False) 

        elif(result == 'numeric'):
            numeric = numeric_settings(False) 

        elif(result == 'quit'):
            return basic + numeric;

all = menu()
if(all != ''):
    vimrc = open(os.path.join(os.path.expanduser("~"), '.vimrc'), 'w')
    print(all, file=vimrc)
