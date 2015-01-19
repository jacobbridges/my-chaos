'''Module for string compression.

This module provides two functions for
compressing and decompressing strings.'''

################################################################################

__version__ = '$Revision: 0 $'
__date__ = 'April 17, 2008'
__author__ = 'Stephen "Zero" Chappell <my.bios@gmail.com>'
__credits__ = '''\
S. Schaub, for introducing me to programming.
B. Brown, for teaching me some math courses.
E. Skogen, for listening to my ideas.'''

################################################################################

import random as _random
import sys as _sys

################################################################################

def encode(key, string, divide=1024):
    'Compress a string.'
    base = len(key) + 1
    array = []
    for index in xrange(0, len(string), divide):
        array.append(_encode(string[index:index+divide], key, base))
    return '\0'.join(array)

def decode(key, string):
    'Decompress a string.'
    base = len(key) + 1
    array = []
    for string in string.split('\0'):
        array.append(_decode(string, key, base))
    return ''.join(array)

################################################################################

def make_key(string):
    'Make key from string.'
    return ''.join(byte for byte in map(chr, xrange(256)) if byte in string)

def minimize(string, divide=1024, random=False):
    'Automate several encoding tasks.'
    key = make_key(string)
    if random:
        key = ''.join(_random.sample(key, len(key)))
    return key, encode(key, string, divide)

################################################################################

def _encode(s, k, b):
    'Private module function.'
    i = 0
    for c in s:
        i *= b
        i += k.index(c) + 1
    s = ''
    while i:
        s = chr(i % 255 + 1) + s
        i /= 255
    return s

def _decode(s, k, b):
    'Private module function.'
    i = 0
    for c in s:
        i *= 255
        i += ord(c) - 1
    s = ''
    while i:
        s = k[i % b - 1] + s
        i /= b
    return s

################################################################################

if __name__ == '__main__':
    _sys.stdout.write('Content-Type: text/plain\n\n')
    _sys.stdout.write(file(_sys.argv[0]).read())
