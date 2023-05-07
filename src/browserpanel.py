import urwid
from panwid import *
import os

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
        return urwid.AttrMap(urwid.LineBox(urwid.ListBox(self.currentWalker), f"{self.currentPath}"), 'body')
    
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
    

