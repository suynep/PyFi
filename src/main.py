import urwid 
import os
import colors

curr = os.listdir('.')
prev = os.listdir('/')

but = []

palette = colors.colors

for c in prev:
    button = urwid.Text(('bright_cyan', c), align='center')

    but.append(urwid.AttrMap(button, 'bg'))

print(palette)

main = urwid.ListBox(urwid.SimpleFocusListWalker(but))
loop = urwid.MainLoop(main, palette)
loop.screen.set_terminal_properties(colors=256)
loop.run()
