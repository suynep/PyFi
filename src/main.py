import urwid 
def exit_on_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()
    
palette = [
    ('banner', 'black', 'light gray'),
    ('streak', 'black', 'dark red'),
    ('bg', 'black', 'dark blue'),
]

txt = urwid.Text(('banner', u"hello world"), align = 'center')

map1 = urwid.AttrMap(txt, 'streak')
fill = urwid.Filler(map1)
map2 = urwid.AttrMap(fill, 'bg')
loop = urwid.MainLoop(map2, palette, unhandled_input=exit_on_q)
# here, the unhandled input is a function that's called
# when the input given by the user is not handled by any widget
# of urwid 
loop.run()