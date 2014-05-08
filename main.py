#! /usr/bin/env python3

import locale, dialog
from dialog import Dialog
import json

# This is almost always a good thing to do at the beginning of your programs.
locale.setlocale(locale.LC_ALL, '')

d = Dialog(dialog="dialog")
# Dialog.set_background_title() requires pythondialog 2.13 or later
d.set_background_title("VIMX")
# For older versions, you can use:
#   d.add_persistent_args(["--backtitle", "My little program"])

# In pythondialog 3.x, you can compare the return code to d.OK, Dialog.OK or
# "ok" (same object). In pythondialog 2.x, you have to use d.DIALOG_OK, which
# is deprecated since version 3.0.0.
menu_file = open('menu.json')
menu_option = json.load(menu_file)
onoff_file = open('onoff.json')
onoff_option = json.load(onoff_file)
numeric_file = open('numeric.json')
numeric_option = json.load(numeric_file)
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

