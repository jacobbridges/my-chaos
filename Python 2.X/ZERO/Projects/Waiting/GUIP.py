class Proxy:

    def __init__(self, obj, name=None):
        self.__obj = obj
        self.__name = obj.__class__.__name__ if name is None else name
        
    def __getattr__(self, name):
        return Proxy(getattr(self.__obj, name), self.__name + '.' + name)
    
    def __call__(self, *args, **kwargs):
        data = self.__obj(*args, **kwargs)
        print '%s(%s)' % (self.__name, ', '.join(map(repr, args) + ['%s=%r' % (key, kwargs[key]) for key in sorted(kwargs.keys())]))
        print 'return', repr(data)
        print '\n', '=' * 40, '\n'
        return data

#######################

import Tkinter

window = lambda: Tkinter.Tk() if Tkinter_default_root is None else Tkinter.Toplevel

class Proxy:

    def __init__(self, obj, parent=None):
        self.__obj = obj
        if parent is None:
            self.__name = obj.__class__.__name__
            self.__window = window()
        else:
            self.__name, self.__window = parent

    def __getattr__(self, name):
        return Proxy(getattr(self.__obj, name), (self.__name + '.' + name, self.__window))

    def __call__(self, *args, **kwargs):
        pass
