#!/usr/bin/env python
import os
import urwid
import panwid
import colors
from datetime import datetime
import panwid.keymap
from browserpanel import BrowserPanel

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


def exit_program(key):
    if key == 'q':
        raise urwid.ExitMainLoop()

def main():
    home_path = os.path.expanduser('~')
    p1 = BrowserPanel(home_path)
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

