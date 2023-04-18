import urwid 
import os
import colors

curr = os.listdir('.')
prev = os.listdir('/')

dir = []
dir.append(curr)
dir.append(prev)
but = []
# this comment is added by bikesh

palette = colors.colors

def show_dir(dir_path):
    for c in dir_path:
        txt = urwid.Text(('bright_cyan', c), align='center')
        but.append(urwid.AttrMap(txt, 'bg'))

show_dir(prev)
def key_press(key):
    x = 0
    if key in ('j'):
        show_dir(dir[x%2])
        x += 1

print(palette)

main = urwid.ListBox(urwid.SimpleFocusListWalker(but))
loop = urwid.MainLoop(main, palette, unhandled_input=key_press)
loop.screen.set_terminal_properties(colors=256)
loop.run()
