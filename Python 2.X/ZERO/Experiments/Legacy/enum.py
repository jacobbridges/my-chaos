# allows quick, easy creation of enumeration objects
def enum(*names):
    class enum(object):
        def __setattr__(self, parameter, value):
            raise AttributeError
        def __delattr__(self, parameter):
            raise AttributeError
    obj = enum()
    for value, parameter in enumerate(names):
        obj.__dict__[parameter] = value
    return obj
