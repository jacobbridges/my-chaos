'''Module that implements SPICE.

This module provides access to a standardized implementation
of SPICE (Stephen's Power-Inspired, Computerized Encryption).'''

################################################################################

__version__ = '$Revision: 0 $'
__date__ = 'March 19, 2008'
__author__ = 'Stephen "Zero" Chappell <my.bios@gmail.com>'
__credits__ = '''\
T. Parker, for testing code that led to this module.
A. Baddeley, for contributing to the random module.
R. Hettinger, for adding support for two core generators.'''

################################################################################

import random as _random
import sys as _sys

################################################################################

def major():
    'Create a new Major Key.'
    return ''.join(map(chr, _random.sample(xrange(256), 256)))

def minor():
    'Create a new Minor Key.'
    sample = _random.sample(range(4) * 64, 256)
    return ''.join(map(chr, ((sample[index * 4] << 6) + (sample[index * 4 + 1] << 4) + (sample[index * 4 + 2] << 2) + sample[index * 4 + 3] for index in xrange(64))))

def encode(source, destination, major_key, minor_key):
    'Encode from source to destination via Major and Minor Keys.'
    _check_major(major_key)
    _check_minor(minor_key)
    map_1 = map(ord, major_key)
    map_2 = _setup_minor(minor_key)
    character = source.read(1)
    while character:
        byte = map_1[ord(character)]
        for shift in xrange(6, -2, -2):
            destination.write(map_2[(byte >> shift) & 3][_random.randrange(64)])
        character = source.read(1)
    destination.flush()

def decode(source, destination, major_key, minor_key):
    'Decode from source to destination via Major and Minor Keys.'
    _check_major(major_key)
    _check_minor(minor_key)
    map_1 = [(byte >> shift) & 3 for byte in map(ord, minor_key) for shift in xrange(6, -2, -2)]
    map_2 = _setup_major(major_key)
    double_word = source.read(4)
    while double_word:
        destination.write(map_2[(map_1[ord(double_word[0])] << 6) + (map_1[ord(double_word[1])] << 4) + (map_1[ord(double_word[2])] << 2) + map_1[ord(double_word[3])]])
        double_word = source.read(4)
    destination.flush()

################################################################################

def _check_major(major_key):
    'Private module function.'
    assert isinstance(major_key, str) and len(major_key) == 256
    for character in map(chr, xrange(256)):
        assert character in major_key

def _check_minor(minor_key):
    'Private module function.'
    assert isinstance(minor_key, str) and len(minor_key) == 64
    indexs = [(byte >> shift) & 3 for byte in map(ord, minor_key) for shift in xrange(6, -2, -2)]
    for index in xrange(4):
        assert indexs.count(index) == 64

def _setup_minor(minor_key):
    'Private module function.'
    map_2 = [[], [], [], []]
    for byte, index in enumerate((byte >> shift) & 3 for byte in map(ord, minor_key) for shift in xrange(6, -2, -2)):
        map_2[index].append(chr(byte))
    return map_2

def _setup_major(major_key):
    'Private module function.'
    map_2 = [None] * 256
    for byte, index in enumerate(map(ord, major_key)):
        map_2[index] = chr(byte)
    return map_2

################################################################################

if __name__ == '__main__':
    _sys.stdout.write('Content-Type: text/plain\n\n')
    _sys.stdout.write(file(_sys.argv[0]).read())
