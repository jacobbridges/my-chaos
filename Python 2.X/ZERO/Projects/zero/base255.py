'''Module for string conversion.

This module provides two functions that allow
strings to be encoded and decoded in base 255.'''

################################################################################

__version__ = '$Revision: 0 $'
__date__ = 'April 28, 2008'
__author__ = 'Stephen "Zero" Chappell <my.bios@gmail.com>'
__credits__ = '''\
S. Schaub, for introducing me to programming.
B. Brown, for teaching me some math courses.
E. Skogen, for listening to my ideas.'''

################################################################################

import sys as _sys

################################################################################

def encode(string, divide=1024):
    'Encode a string to base 255.'
    array = []
    for index in xrange(0, len(string), divide):
        array.append(_encode(string[index:index+divide]))
    return '\1'.join(array)

def decode(string):
    'Decode a string from base 255.'
    array = []
    for string in string.split('\1'):
        array.append(_decode(string))
    return ''.join(array)

################################################################################

def _encode(s):
    'Private module function.'
    i = 0
    for c in s:
        i *= 257
        i += ord(c) + 1
    s = ''
    while i:
        s = chr(i % 254 + 2) + s
        i /= 254
    return s

def _decode(s):
    'Private module function.'
    i = 0
    for c in s:
        i *= 254
        i += ord(c) - 2
    s = ''
    while i:
        s = chr(i % 257 - 1) + s
        i /= 257
    return s

################################################################################

if __name__ == '__main__':
    _sys.stdout.write('Content-Type: text/plain\n\n')
    _sys.stdout.write(file(_sys.argv[0]).read())
