import sys, _tkinter
if sys.platform == 'win32':
    import FixTk
tk = _tkinter.create()
tk.evalfile(r'C:\Python25\tcl\tk8.4\demos\widget')
tk.mainloop()
