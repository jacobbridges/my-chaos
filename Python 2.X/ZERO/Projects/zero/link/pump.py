'''Module for automatically replying to queries.

This modules provides support for automating replies in
SPOTS and has several classes to assist in this process.'''

################################################################################

__version__ = '$Revision: 0 $'
__date__ = 'September 29, 2007'
__author__ = 'Stephen "Zero" Chappell <my.bios@gmail.com>'
__credits__ = '''\
G. Rossum, for allowing thread support in Python.
D. Wooster, for giving me reason to learn sockets.
T. Parker, for testing code that led to this module.'''

################################################################################

import cPickle as _cPickle
import inspect as _inspect
import security as _security
import sys as _sys
import thread as _thread
import traceback as _traceback

################################################################################

PROTOCOL_DOCUMENTATION = '''\
Query
    Mode
        0 = Quit
        1 = Builtin
        2 = Dynamic
    Name
        Quit
            "quit"
        Builtin
            "t" = Title
            "n" = Name
            "d" = Doc
            "l" = List
            "s" = Signature
            "h" = Help
        Dynamic
            name
    Args
        Quit
            ()
        Builtin
            "tndl" = ()
            "sh" = (name,)
        Dynamic
            *args
    Kwargs
        Quit
            {}
        Builtin
            {}
        Dynamic
            **kwargs
==============================
Reply
    Mode
        0 = Error
        1 = Reply
    Data
        Error Instance
        Return Value'''
    
################################################################################

def synchronize(obj):
    'Return a synchronized object.'
    return _Synchronizer(obj, _thread.allocate_lock())

################################################################################

def _get_signature(obj):
    'Private module function.'
    return _inspect.formatargspec(*_inspect.getargspec(obj))

################################################################################

class _Synchronizer:

    '_Synchronizer(obj, lock) -> _Synchronizer'

    def __init__(self, obj, lock):
        'Initialize the _Synchronizer object.'
        self.__obj = obj
        self.__lock = lock
        self.__doc__ = _inspect.getdoc(obj)
        try:
            if self.__doc__ is None:
                self.__doc__ = _get_signature(obj)
            else:
                self.__doc__ += '\n' + _get_signature(obj)
        except:
            pass

    def __getattr__(self, name):
        'Return a synchronized attribute.'
        return _Synchronizer(getattr(self.__obj, name), self.__lock)

    def __call__(self, *args, **kwargs):
        'Execute serialized call on object.'
        self.__lock.acquire()
        try:
            data = self.__obj(*args, **kwargs)
        finally:
            self.__lock.release()
        return data

################################################################################

class PumpError(Exception):
    
    'Base Class For All Pump Errors'

    def __repr__(self):
        'Return the object\'s representation.'
        indent = ' ' * (len(self.__class__.__name__) + 1)
        lines = [line for line in str(self).split('\n') if line]
        data = '%s(%s' % (self.__class__.__name__, lines[0])
        for line in lines[1:]:
            data += '\n' + indent + line
        return data + ')'

class PumpExecutionError(PumpError):
    'Base Class For All Pump Execution Errors'
class PumpExecutionExternalError(PumpExecutionError):
    'Raised When External Function Fails'
class PumpExecutionInternalError(PumpExecutionError):
    'Raised When Internal Function Fails'
class PumpLookupError(PumpError):
    'Base Class For All Pump Lookup Errors'
class PumpLookupLibraryError(PumpLookupError):
    'Raised When Lookup Fails With Library'
class PumpLookupSecurityError(PumpLookupError):
    'Raised When Lookup Fails With Security'
class PumpProtocolError(PumpError):
    'Base Class For All Pump Protocol Errors'
class PumpProtocolTypeError(PumpProtocolError):
    'Raised When Query Has Wrong Argument Types'
class PumpProtocolValueError(PumpProtocolError):
    'Raised When Query Has Wrong Argument Values'
class PumpReplyError(PumpError):
    'Base Class For All Pump Reply Errors'
class PumpReplyPickleError(PumpReplyError):
    'Raised When Reply Cannot Be Pickled'
class PumpReplyShutdownError(PumpReplyError):
    'Raised When Pump Is Shutting Down'

################################################################################

class Library:

    'Library() -> Library'

    def __init__(self):
        'Initialize the Library object.'
        self.__name = {}
        self.__attr = {}

    def __repr__(self):
        'Return the object\'s representation.'
        return 'Library()'

    def __getitem__(self, key):
        'Acquire an object from the Library.'
        _security.assert_(key)
        if key in self.__name:
            return self.__name[key]
        attrs = key.count('.')
        for index in xrange(attrs - 1, -1, -1):
            if index in self.__attr:
                for name in self.__attr[index]:
                    if self.__in(name, key):
                        obj = self.__name[name]
                        try:
                            for attr in key.rsplit('.', attrs - index)[1:]:
                                obj = getattr(obj, attr)
                            return obj
                        except:
                            raise LookupError, 'Object not found.'
        raise LookupError, 'Object not found.'

    def __in(self, name, key):
        'Private class method.'
        for a, b in zip(name.split('.'), key.split('.')):
            if a != b:
                return False
        return True

    def __setitem__(self, key, value):
        'Add an object to the Library.'
        _security.assert_(key)
        if key not in self.__name:
            index = key.count('.')
            if index in self.__attr:
                self.__attr[index].append(key)
            else:
                self.__attr[index] = [key]
        self.__name[key] = value

    def __delitem__(self, key):
        'Remove an object from the Library.'
        _security.assert_(key)
        assert key in self.__name, 'Object not found.'
        del self.__name[key]
        index = key.count('.')
        if len(self.__attr[index]) == 1:
            del self.__attr[index]
        else:
            self.__attr[index].remove(key)

    def keys(self):
        'Return list of installed objects.'
        return sorted(self.__name.keys())

################################################################################

class Pump:

    'Pump(QRI, TND, library, security, onquit, onexit, onerror) -> Pump'

    TIMEOUT = 1

    def __init__(self, QRI, TND, library, security, onquit, onexit, onerror):
        'Initialize the Pump object.'
        self.__QRI = QRI
        self.__TND = TND
        self.__library = library
        self.__security = security
        self.__onquit = onquit
        self.__onexit = onexit
        self.__onerror = onerror
        self.__start()

    def __repr__(self):
        'Return the object\'s representation.'
        return 'Pump(%r, %r, %r, %r, %r, %r, %r)' % (self.__QRI,
                                                     self.__TND,
                                                     self.__library,
                                                     self.__security,
                                                     self.__onquit,
                                                     self.__onexit,
                                                     self.__onerror)

    def __start(self):
        'Private class method.'
        self.__active = True
        self.__lock = _thread.allocate_lock()
        _thread.start_new_thread(self.__run, ())

    def kill(self):
        'Arrange for Pump to shutdown.'
        self.__active = False

    def __run(self):
        'Private class method.'
        args = self.__query()
        while self.__active:
            if args is not None:
                _thread.start_new_thread(self.__process, args)
            args = self.__query()
        self.__shutdown(args)

    def __query(self):
        'Private class method.'
        try:
            return self.__QRI.query(self.TIMEOUT)
        except Warning:
            return None
        except (EOFError, IOError), error:
            self.__error(error)

    def __reply(self, ID, obj):
        'Private class method.'
        try:
            self.__QRI.reply(ID, obj)
        except _cPickle.UnpickleableError:
            self.__raise(ID,
                         PumpReplyPickleError,
                         _traceback.format_exc())
        except (EOFError, IOError), error:
            self.__error(error)

    def __error(self, error):
        'Private class method.'
        self.__lock.acquire()
        if self.__active:
            self.kill()
            try:
                self.__onerror(self, error)
            except:
                _traceback.print_exc()
        self.__lock.release()

    def __shutdown(self, args):
        'Private class method.'
        while args is not None:
            ID, obj = args
            self.__raise(ID,
                         PumpReplyShutdownError,
                         'Pump is currently being shutdown.')
            args = self.__query()
        self.__onexit(self)

    def __process(self, ID, obj):
        'Private class method.'
        mode, name, args, kwargs = self.__validate(ID, obj)
        if mode == 0:
            self.__quit(ID)
        elif mode == 1:
            self.__builtin(ID, name, args)
        else:
            self.__dynamic(ID, name, args, kwargs)

    def __validate(self, ID, obj):
        'Private class method.'
        self.__validate_query(ID, obj)
        mode, name, args, kwargs = obj
        self.__validate_mode(ID, mode)
        self.__validate_name(ID, name, mode)
        self.__validate_args(ID, args, mode, name)
        self.__validate_kwargs(ID, kwargs, mode)
        return mode, name, args, kwargs

    def __validate_query(self, ID, obj):
        'Private class method.'
        if not isinstance(obj, tuple):
            self.__raise(ID,
                         PumpProtocolTypeError,
                         'Query is not a tuple.')
        if len(obj) != 4:
            self.__raise(ID,
                         PumpProtocolValueError,
                         'Query length is not four.')

    def __validate_mode(self, ID, mode):
        'Private class method.'
        if not isinstance(mode, int):
            self.__raise(ID,
                         PumpProtocolTypeError,
                         'Mode is not an integer.')
        if mode not in (0, 1, 2):
            self.__raise(ID,
                         PumpProtocolValueError,
                         'Mode is not 0, 1, or 2.')

    def __validate_name(self, ID, name, mode):
        'Private class method.'
        if not isinstance(name, str):
            self.__raise(ID,
                         PumpProtocolTypeError,
                         'Name is not a string.')
        if mode == 0:
            if name != 'quit':
                self.__raise(ID,
                             PumpProtocolValueError,
                             'Name is not "quit" value.')
        elif mode == 1:
            if name not in tuple('tndlsh'):
                self.__raise(ID,
                             PumpProtocolValueError,
                             'Name is not an internal function.')
        else:
            self.__validate_security(ID, name)

    def __validate_args(self, ID, args, mode, name):
        'Private class method.'
        if not isinstance(args, tuple):
            self.__raise(ID,
                         PumpProtocolTypeError,
                         'Args is not a tuple.')
        if mode == 0:
            if len(args) != 0:
                self.__raise(ID,
                             PumpProtocolValueError,
                             'Args length is not zero.')
        elif mode == 1:
            if name in tuple('sh'):
                if len(args) != 1:
                    self.__raise(ID,
                                 PumpProtocolValueError,
                                 'Args length is not one.')
                if not isinstance(args[0], str):
                    self.__raise(ID,
                                 PumpProtocolTypeError,
                                 'Arg is not a string.')
                self.__validate_security(ID, args[0])
            else:
                if len(args) != 0:
                    self.__raise(ID,
                                 PumpProtocolValueError,
                                 'Args length is not zero.')

    def __validate_kwargs(self, ID, kwargs, mode):
        'Private class method.'
        if not isinstance(kwargs, dict):
            self.__raise(ID,
                         PumpProtocolTypeError,
                         'Kwargs is not a dictionary.')
        if 0 <= mode <= 1 and len(kwargs) != 0:
            self.__raise(ID,
                         PumpProtocolValueError,
                         'Kwargs length is not zero.')

    def __validate_security(self, ID, name):
        'Private class method.'
        try:
            if not self.__security(name):
                self.__raise(ID,
                             PumpLookupSecurityError,
                             'Name is not allowed by security.')
        except:
            self.__raise(ID,
                         PumpLookupSecurityError,
                         _traceback.format_exc())

    def __raise(self, ID, error, message):
        'Private class method.'
        self.__reply(ID, (0, error(message)))
        if self.__active:
            _thread.exit()

    def __quit(self, ID):
        'Private class method.'
        try:
            data = self.__onquit(self)
        except:
            self.__raise(ID,
                         PumpExecutionExternalError,
                         _traceback.format_exc())
        self.__reply(ID, (1, data))

    def __builtin(self, ID, name, args):
        'Private class method.'
        if name == 't':
            self.__reply(ID, (1, self.__TND.title))
        elif name == 'n':
            self.__reply(ID, (1, self.__TND.name))
        elif name == 'd':
            self.__reply(ID, (1, self.__TND.doc))
        elif name == 'l':
            self.__reply_list(ID)
        elif name == 's':
            self.__reply_signature(ID, args[0])
        else:
            self.__reply_help(ID, args[0])

    def __reply_list(self, ID):
        'Private class method.'
        array = [key for key in self.__library.keys() if self.__security(key)]
        self.__reply(ID, (1, array))

    def __reply_signature(self, ID, name):
        'Private class method.'
        obj = self.__get(ID, name)
        try:
            signature = _get_signature(obj)
        except:
            self.__raise(ID,
                         PumpExecutionInternalError,
                         _traceback.format_exc())
        self.__reply(ID, (1, signature))
                         

    def __reply_help(self, ID, name):
        'Private class method.'
        obj = self.__get(ID, name)
        try:
            doc = _inspect.getdoc(obj)
        except:
            self.__raise(ID,
                         PumpExecutionInternalError,
                         _traceback.format_exc())
        self.__reply(ID, (1, doc))

    def __dynamic(self, ID, name, args, kwargs):
        'Private class method.'
        obj = self.__get(ID, name)
        try:
            data = obj(*args, **kwargs)
        except:
            self.__raise(ID,
                         PumpExecutionExternalError,
                         _traceback.format_exc())
        self.__reply(ID, (1, data))

    def __get(self, ID, name):
        'Private class method.'
        try:
            return self.__library[name]
        except:
            self.__raise(ID,
                         PumpLookupLibraryError,
                         _traceback.format_exc())

################################################################################

class TND(object):

    'TND(title, name, doc) -> TND'

    def __init__(self, title, name, doc):
        'Initialize the TND object.'
        self.title = title
        self.name = name
        self.doc = doc

    def __repr__(self):
        'Return the object\'s representation.'
        return 'TND(%r, %r, %r)' % (self.title, self.name, self.doc)

    def __get_title(self):
        'Private class method.'
        return self.__title

    def __set_title(self, value):
        'Private class method.'
        assert isinstance(value, str), 'Title must be a string.'
        self.__title = value

    def __get_name(self):
        'Private class method.'
        return self.__name

    def __set_name(self, value):
        'Private class method.'
        assert isinstance(value, str), 'Name must be a string.'
        self.__name = value

    def __get_doc(self):
        'Private class method.'
        return self.__doc

    def __set_doc(self, value):
        'Private class method.'
        assert isinstance(value, str), 'Doc must be a string.'
        self.__doc = value

    title = property(__get_title, __set_title, doc='Value of title.')
    name = property(__get_name, __set_name, doc='Value of name.')
    doc = property(__get_doc, __set_doc, doc='Value of doc.')

################################################################################

if __name__ == '__main__':
    _sys.stdout.write('Content-Type: text/plain\n\n')
    _sys.stdout.write(file(_sys.argv[0]).read())
