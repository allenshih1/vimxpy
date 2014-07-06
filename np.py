#!/usr/bin/env python

import npyscreen
import json
import os
from paser.paser import vimrcPaser
from paser.search import searchInVimrc

class OptForm(npyscreen.Form):
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
                self.numericResult.append(self.add(npyscreen.TitleText, name = key, value = opt["content"]))

        self.onoffResult = self.add(npyscreen.MultiSelect, value = selected, scroll_exit=True, values = self.onoff)

    def afterEditing(self):
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

class MenuForm(npyscreen.ActionForm):
    def create(self):
        self.add(MenuMultiLineAction, values = self.parentApp.displayDict.keys(), scroll_exit=True)

    def on_ok(self):
        self.parentApp.switchForm(None)

    def on_ok(self):
        self.parentApp.switchForm(None)

class MenuMultiLineAction(npyscreen.MultiLineAction):
    def actionHighlighted(self, act_on_this, key_press):
        self.parent.parentApp.currentOpt = act_on_this
        self.parent.parentApp.switchForm('opt')

class VimXApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.currentOpt = None
        self.readOpt()
        self.categorizeOpt()
        self.addFormClass('opt', OptForm)
        self.addForm('MAIN', MenuForm, name = "VIMX")

    def readOpt(self):
        self.f = open("options.json", "r")
        self.opts = json.load(self.f)

    def categorizeOpt(self):
        vimrcPath = os.path.expanduser("~/.vimrc2")
        fVimrc = open( vimrcPath, "r")
        userOpts = vimrcPaser(fVimrc, 'set')
        self.displayDict = dict()
        for key in self.opts:
            opt = self.opts[key]
            result = searchInVimrc(key, userOpts, "option")
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
