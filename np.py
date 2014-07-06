#!/usr/bin/env python

import npyscreen
import curses
import json
import os
import re
from paser.paser import vimrcPaser

class OptForm(npyscreen.ActionForm):
    def create(self):
        cat = self.parentApp.currentOpt
        opts = self.parentApp.displayDict[cat]
        self.name = cat

        self.onoff = []
        selected = []
        self.numeric = []
        self.numericResult = []
        i = 0
        for key in opts:
            opt = opts[key]
            if opt["type"] == "onoff":
                self.onoff.append(key)
                if(opt["content"] == True):
                    selected.append(i)
                i += 1
            elif opt["type"] == "numeric":
                self.numeric.append(key)
                self.numericResult.append(self.add(TitleTextWithHelp, name = key, value = opt["content"]))

        self.onoffResult = self.add(MultiSelectWithHelp, value = selected, scroll_exit=True, values = self.onoff)

    def display_menu_advert_at(self):
        return self.lines-1, 1

    def draw_form(self):
        super(OptForm, self).draw_form()
        menu_advert = " ^L: Option Descriptions "
        y, x = self.display_menu_advert_at()
        if isinstance(menu_advert, bytes):
            menu_advert = menu_advert.decode('utf-8', 'replace')
        self.add_line(y, x,
            menu_advert,
            self.make_attributes_list(menu_advert, curses.A_NORMAL),
            self.columns - x - 1
            )

    def on_ok(self):
        opts = self.parentApp.opts
        for i in range(len(self.onoff)):
            if i in self.onoffResult.value:
                tmp = True
            else:
                tmp = False
            opts[self.onoff[i]]["content"] = tmp

        for i in range(len(self.numeric)):
            opts[self.numeric[i]]["content"] = self.numericResult[i].value

        self.parentApp.setNextForm('MAIN')

    def on_cancel(self):
        self.parentApp.setNextForm('MAIN')

class MultiSelectWithHelp(npyscreen.MultiSelect):
    def set_up_handlers(self):
        super(MultiSelectWithHelp, self).set_up_handlers()
        self.handlers.update({'^L': self.h_act_on_help})

    def h_act_on_help(self, ch):
        highlighted = self.values[self.cursor_line]
        npyscreen.notify_confirm((self.parent.parentApp.opts[highlighted]["description"]), title = "Help")

class TitleTextWithHelp(npyscreen.TitleText):
    def set_up_handlers(self):
        super(TitleTextWithHelp, self).set_up_handlers()
        self.handlers.update({'^L': self.h_act_on_help})

    def h_act_on_help(self, ch):
        highlighted = self.name
        npyscreen.notify_confirm((self.parent.parentApp.opts[highlighted]["description"]), title = "Help")

class MenuForm(npyscreen.ActionForm):
    OK_BUTTON_TEXT = 'Save and quit'
    OK_BUTTON_BR_OFFSET = (2, 7)
    CANCEL_BUTTON_TEXT = 'Quit without saving'
    CANCEL_BUTTON_BR_OFFSET = (2, 24)
    def create(self):
        art = open("asciiart.txt", "r")
        for line in art:
            self.add(npyscreen.Textfield, editable = False, value = line)
        self.add(MenuMultiLineAction, values = sorted(self.parentApp.displayDict.keys()), scroll_exit=True)

    def on_ok(self):
        self.parentApp.writeOpt()
        self.parentApp.switchForm(None)

    def on_cancel(self):
        self.parentApp.switchForm(None)

class MenuMultiLineAction(npyscreen.MultiLineAction):
    def actionHighlighted(self, act_on_this, key_press):
        self.parent.parentApp.currentOpt = act_on_this
        self.parent.parentApp.switchForm('opt')

class VimXApp(npyscreen.NPSAppManaged):
    def onStart(self):
        # backup origin vimrc
        self.vimrcPath = os.path.expanduser("~/.vimrc")
        self.bak_vimrcPath = os.path.expanduser("~/.bak_vimrc")
        self.oriVimrc = open( self.vimrcPath, "r")
        wVimrc = open( self.bak_vimrcPath, "w")
        for line in self.oriVimrc:
            wVimrc.write(line)
        # complete backup
        self.currentOpt = None
        self.readOpt()
        self.categorizeOpt()
        self.addFormClass('opt', OptForm)
        self.addForm('MAIN', MenuForm, name = "VIMX")

    def readOpt(self):
        self.f = open("options.json", "r")
        self.opts = json.load(self.f)

    def writeOpt(self):
        self.oriVimrc = open( self.bak_vimrcPath, "r")
        wVimrc = open( self.vimrcPath, "w")
        flag = 0
        for line in self.oriVimrc:
            if flag == 0 and re.search('^\"\"\" vimx begin$', line):
                flag = 1
            elif flag == 1 and re.search('^\"\"\" vimx end$', line):
                flag = 0
            elif flag == 0:
                wVimrc.write(line)
        wVimrc.write('\"\"\" vimx begin\n')
        for opt in self.opts:
            wVimrc.write('set ')
            if self.opts[opt]['type'] == "onoff":
                if self.opts[opt]['content'] == True:
                    wVimrc.write(opt)
                    wVimrc.write("\n")
                elif self.opts[opt]['content'] == False:
                    wVimrc.write("no")
                    wVimrc.write(opt)
                    wVimrc.write("\n")
            elif self.opts[opt]['type'] == "numeric":
                wVimrc.write(opt)
                wVimrc.write("=")
                wVimrc.write(self.opts[opt]['content'])
                wVimrc.write("\n")
        wVimrc.write('\"\"\" vimx end\n')

    def categorizeOpt(self):
        self.oriVimrc = open( self.vimrcPath, "r")
        userOpts = vimrcPaser(self.oriVimrc, 'set')
        self.displayDict = dict()
        for key in self.opts:
            opt = self.opts[key]
            result = userOpts.get(key)
            if result:
                opt["content"] = result["content"]
            else:
                opt["content"] = opt["default"]
            cat = opt["category"]
            if cat in self.displayDict:
                self.displayDict[cat][key] = opt
            else:
                self.displayDict[cat] = {key: opt}

if __name__ == '__main__':
    V = VimXApp()
    V.run()
