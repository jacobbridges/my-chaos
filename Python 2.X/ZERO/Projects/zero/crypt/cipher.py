'''Module for modifying strings.

This module provides several functions for creating named tables,
translating strings in both directions, and partitioning strings.'''

################################################################################

__version__ = '$Revision: 0 $'
__date__ = 'February 11, 2007'
__author__ = 'Stephen "Zero" Chappell <my.bios@gmail.com>'
__credits__ = '''\
S. Schaub, for introducing me to programming.
H. Chappell, for testing code that led to this module.
G. Rossum, for making strings object oriented.'''

################################################################################

import random as _random
import sys as _sys

################################################################################

def key(name=None):
    'Create cipher key.'
    if name is not None:
        _random.seed(name)
    return ''.join(map(chr, _random.sample(xrange(256), 256)))

def cipher(text, key, mode):
    'Create cipher text.'
    if mode:
        mirror = dict((ord(c), chr(i)) for i, c in enumerate(key))
        key = ''.join(mirror.values())
    return text.translate(key)

def qualify(key):
    'Return the quality of a key.'
    master = ''.join(map(chr, xrange(256)))
    slave = master.translate(key)
    Q = 0
    while slave != master:
        slave = slave.translate(key)
        Q += 1
    return Q

def partition(text, size):
    'Divide text into partitions.'
    return (text[index:index+size] for index in xrange(0, len(string), size))

################################################################################

if __name__ == '__main__':
    _sys.stdout.write('Content-Type: text/plain\n\n')
    _sys.stdout.write(file(_sys.argv[0]).read())
