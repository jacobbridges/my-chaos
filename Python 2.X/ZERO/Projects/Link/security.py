'''Module for assistance with network Security.

This module provides three classes to be used in conjunction
with a Link Processor to check permissions on code execution.'''

################################################################################

__version__ = '$Revision: 0 $'
__date__ = 'September 27, 2007'
__author__ = 'Stephen "Zero" Chappell <my.bios@gmail.com>'
__credits__ = '''\
S. Schaub, for introducing me to programming.
D. Wooster, for giving me reason to learn sockets.
T. Parker, for testing code that led to this module.'''

################################################################################

import keyword as _keyword
import sys as _sys

################################################################################

def init(*reserved):
    'Initialize the name-checking system.'
    global assert_
    assert_ = _Assert(*reserved)

################################################################################

class _Assert:

    '_Assert(*reserved) -> _Assert'

    T = ''.join(map(chr, xrange(256)))
    L = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz'
    D = '0123456789' + L

    def __init__(self, *reserved):
        'Initialize the _Assert object.'
        self.__reserved = reserved

    def __repr__(self):
        'Return the object\'s representation.'
        return '_Assert(%s)' % ', '.join(map(repr, self.__reserved))

    def __call__(self, name):
        'Assert validity of name.'
        words = name.split('.')
        assert words[0] not in self.__reserved, '"%s" is a reserved word.' % words[0]
        for word in words:
            assert self.__identifier(word), '"%s" is not an identifier.' % word
            assert not _keyword.iskeyword(word), '"%s" is a keyword.' % word

    def __identifier(self, word):
        'Private class method.'
        return word and word[0] in self.L and not word.translate(self.T, self.D)

################################################################################

class _Rule:

    '_Rule(name, allow) -> _Rule'

    def __init__(self, name, flag):
        'Initialize the _Rule object.'
        assert isinstance(flag, bool), '"flag" must be a boolean.'
        assert_(name)
        self.__name = name
        self.__flag = flag

    def __repr__(self):
        'Return the object\'s representation.'
        return '%s(%r, %r)' % (self.__class__.__name__, self.__name, self.__flag)

    def __eq__(self, other):
        'Check if objects are equal.'
        return isinstance(other, self.__class__) and other.__name == self.__name

    def __nonzero__(self):
        'Return the permission flag.'
        return self.__flag

    def __len__(self):
        'Return number of attributes.'
        return self.__name.count('.')

    def __contains__(self, item):
        'Check for a partial name match.'
        for a, b in zip(self.__name.split('.'), item.split('.')):
            if a != b:
                return False
        return True

class Apply(_Rule): pass
class GetAttr(_Rule): pass

################################################################################

class Security(object):

    'Security(default) -> Security'

    def __init__(self, default):
        'Initialize the Security object.'
        assert isinstance(default, bool), '"default" must be a boolean.'
        self.__default = default
        self.__name = {}
        self.__call = {}
        self.__attr = {}

    def __repr__(self):
        'Return the object\'s representation.'
        return 'Security(%r)' % self.__default

    def __call__(self, name):
        'Return permissions for name.'
        assert_(name)
        attrs = name.count('.')
        if attrs in self.__call:
            for rule in self.__call[attrs]:
                if name in rule:
                    return bool(rule)
        for attrs in xrange(attrs - 1, -1, -1):
            if attrs in self.__attr:
                for rule in self.__attr[attrs]:
                    if name in rule:
                        return bool(rule)
        return self.__default

    def __setitem__(self, key, value):
        'Add a Rule to Security.'
        assert isinstance(value, (Apply, GetAttr)), 'Value is of wrong type.'
        if key in self.__name:
            del self[key]
        for name, rule in self.__name.items():
            if rule == value:
                del self[name]
                break
        self.__name[key] = value
        table = self.__call if isinstance(value, Apply) else self.__attr
        if len(value) in table:
            table[len(value)].append(value)
        else:
            table[len(value)] = [value]

    def __delitem__(self, key):
        'Remove a Rule from Security.'
        assert key in self.__name, 'Rule not found.'
        rule = self.__name[key]
        del self.__name[key]
        table = self.__call if isinstance(rule, Apply) else self.__attr
        if len(table[len(rule)]) == 1:
            del table[len(rule)]
        else:
            table[len(rule)].remove(rule)

    def __get_default(self):
        'Private class method.'
        return self.__default

    def __set_default(self, value):
        'Private class method.'
        assert isinstance(value, bool), '"default" must be a boolean.'
        self.__default = value

    default = property(__get_default, __set_default, doc='Backup setting.')

################################################################################

if __name__ == '__main__':
    _sys.stdout.write('Content-Type: text/plain\n\n')
    _sys.stdout.write(file(_sys.argv[0]).read())
