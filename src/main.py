import urwid

txt = urwid.Text(u"Hi")
fill = urwid.Filler(txt, 'top')
loop = urwid.MainLoop(fill)
loop.run()
