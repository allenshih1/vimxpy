#!/usr/bin/env python

import npyscreen
import json

class OptForm(npyscreen.Form):
    def create(self):
        cat = self.parentApp.currentOpt
        opts = self.parentApp.displayDict[cat]
        self.name = cat

        onoff = []
        selected = []
        numeric = []
        i = 0
        for opt in opts:
            if opt["type"] == "onoff":
                onoff.append(opt["option"])
                if(opt["content"] == True):
                    selected.append(i)
                i += 1
            elif opt["type"] == "numeric":
                self.add(npyscreen.TitleText, name = opt["option"], value = opt["content"])

        self.add(npyscreen.MultiSelect, value = selected, scroll_exit=True, values = onoff)

    def afterEditing(self):
        self.parentApp.setNextForm('MAIN')

class MenuForm(npyscreen.Form):
    def create(self):
        self.add(MenuMultiLineAction, values = self.parentApp.displayDict.keys())

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
        self.displayDict = dict()
        for opt in self.opts:
            opt["content"] = opt["default"]
            cat = opt["category"]
            if cat in self.displayDict:
                self.displayDict[cat].append(opt)
            else:
                self.displayDict[cat] = [opt]

if __name__ == '__main__':
    V = VimXApp()
    V.run()
