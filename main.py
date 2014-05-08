#! /usr/bin/env python3

import locale, dialog
from dialog import Dialog
import json

locale.setlocale(locale.LC_ALL, '')
d = Dialog(dialog="dialog")
d.set_background_title("VIMX")

def parser(opt, typ):
    r = []
    if typ == 'onoff':
        for a in opt:
            r.append([a['option'], a['description'], a['default']])
    if typ == 'numeric':
        for a in opt:
            r.append([a['option'], a['default']])
    return r
    

menu_file = open('menu.json')
menu_option = json.load(menu_file)
onoff_file = open('onoff.json')
onoff_option = json.load(onoff_file)
onoff_option = parser(onoff_option, 'onoff')
numeric_file = open('numeric.json')
numeric_option = json.load(numeric_file)
numeric_option = parser(numeric_option, 'numeric')

while True:
    code, tag = d.menu("VIMX",
                       choices=menu_option)
    if code == d.CANCEL:
        break

    if tag == "onoff":
    
        # We could put non-empty items here (not only the tag for each entry)
        code, tags = d.checklist("Basic On Off Settings",
                                 choices=onoff_option,
                                 )
        if code == d.OK:
            # 'tags' now contains a list of the toppings chosen by the user
                                 title="Do you prefer ham or spam?",
    elif tag == "numeric":
        code, tag, new_item_text = d.inputmenu("Numeric Settings",
                                choices=numeric_option)
        if code == d.OK:
            # 'tag' is now either "(1)" or "(2)"
            pass

