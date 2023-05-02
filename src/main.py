#!/usr/bin/env python
import os
import urwid
import panwid
import colors
from datetime import datetime
import panwid.keymap

panwid.keymap.KEYMAP_GLOBAL = {
    "movement": {
        "k": "up",
        "j": "down",
        "h": "left",
        "l": "right",
        "page up": "page up",
        "page down": "page down",
        "ctrl up": ("cycle", [1]),
        "ctrl down": ("cycle", [-1]),
        "home": "home",
        "end": "end",
        "/": "complete prefix",
        "?": "complete substring",
        "ctrl p": "complete_prev",
        "ctrl n": "complete_next",
    }
}
PALETTE=colors.colors
palette = [
    (None,  'light gray', 'black'),
    ('reversed', 'standout', ''),
    ('body', 'dark red', 'white'),
    ('bodyrev', 'black', 'white'),
    ('dirs', 'black', 'light red'),
    ('dirsrev', 'white', 'dark red'),
    ('bg', 'black', 'dark blue'),
    ("reveal_focus","black","yellow"),
    ("text_highlight", "yellow,bold",""),]

from panwid.keymap import *

class BrowserPanel(KeymapMovementMixin, urwid.WidgetPlaceholder):
    def __init__(self, path):
        self.rootPath = '/'
        self.previousPath = self.rootPath
        self.currentPath = path
        self.fileList = sorted(os.listdir(self.currentPath))
        self.currentHighlight = self.currentPath
        self.currentWalker = None
        body = self.create_buttons()
        super(BrowserPanel, self).__init__(body)

    def update_file_list(self, choice):
        if choice == '..':
            newPath = os.path.dirname(self.currentPath)
        else:
            newPath = os.path.join(os.path.join(self.currentPath, choice))
        if os.path.isdir(newPath):
            self.previousPath = self.currentPath
            self.currentPath = newPath
        try:
            self.fileList = os.listdir(self.currentPath)
        except:
            self.currentPath = self.previousPath
            self.fileList = os.listdir(self.currentPath)
        if self.currentPath != '/':
            self.fileList.insert(0, '..')

    def create_buttons(self):
        body = []
        for oneFile in sorted(self.fileList):
            button = urwid.Button(oneFile)
            if os.path.isdir(os.path.join(self.currentPath, oneFile)): # check if the dir exists
                urwid.connect_signal(button, 'click', self.update_body, oneFile) # standard signal handling
                body.append(urwid.AttrMap(button, 'dirs', focus_map='dirsrev'))
            else:
                body.append(urwid.AttrMap(button, None, focus_map='bodyrev'))
        self.currentWalker = urwid.SimpleFocusListWalker(body)
        self.currentHighlight = self.currentWalker.get_focus()
        return urwid.AttrMap(urwid.LineBox(urwid.ListBox(
list_walker), f"{self.currentPath} path"), 'body')
    
    def update_body(self, button, choice):
        self.update_file_list(choice)
        self.original_widget = self.create_buttons()
    
    def handle_input(self, input):
    	if input == 'q':
        	raise urwid.ExitMainLoop()
    	elif input == 'c':
        	self.create_file()
    	elif input == 'd':
        	self.delete_file()
    	elif input == 'r':
        	self.rename_file()
    	elif input == 'm':
        	self.copy_file()
    	else:
        	self.change_dir(input)

    def callback(self):
       index = self.currentWalker.get_focus()[1] 
       self.display_text()
    
  
  # def create_file():
   	

def exit_program(key):
    if key == 'q':
        raise urwid.ExitMainLoop()

def main():
    home_path = os.path.expanduser('~')
    p1 = BrowserPanel('/')
    p2 = BrowserPanel(home_path)
    p3 = urwid.Filler(urwid.Text(home_path))
    print(p1.currentHighlight)
    sub_main = urwid.Columns([p1, p2, p3])
    title = "PyFi: A terminal based file manager in Python"
    today = datetime.now()
    today_f  = today.strftime("%d/%m/%Y %H:%M:%S")
    header_t = urwid.AttrMap(urwid.Text(('text_highlight', f"{title}")), 'reveal_focus')
    footer_t= urwid.AttrMap(urwid.Text(('text_highlight', f"{today_f}")), 'reveal_focus')
    main_frame = urwid.Frame(sub_main, header=header_t, footer=footer_t)
    loop = urwid.MainLoop(main_frame, palette, unhandled_input=exit_program)
    loop.run()

if __name__ == '__main__':
    main()

