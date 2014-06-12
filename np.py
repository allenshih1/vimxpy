#!/usr/bin/env python3
import npyscreen

class MainForm(npyscreen.Form):
    def create(self):
        self.add(npyscreen.TitleFixedText, name = "Tab:")
        self.add(npyscreen.TitleText, name = "tabstop:", value="8")
        self.add(npyscreen.TitleText, name = "shiftwidth:", value="8")
        self.result = self.add(npyscreen.MultiSelect, scroll_exit=True, values = ['expandtab'])

    def afterEditing(self):
        self.parentApp.setNextForm(None)

class VimXApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.registerForm('MAIN', MainForm())

if __name__ == '__main__':
    V = VimXApp()
    V.run()
