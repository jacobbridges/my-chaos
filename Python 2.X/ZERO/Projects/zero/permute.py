'''Module for efficient data permutations.

This module provides functions that allow permutations over a
data set of any size while using as little memory as possible.'''

################################################################################

__version__ = '$Revision: 0 $'
__date__ = 'July 4, 2007'
__author__ = 'Stephen "Zero" Chappell <my.bios@gmail.com>'
__credits__ = '''\
S. Schaub, for introducing me to programming.
H. Chappell, for assisting a study of passwords.
J. Chappell, for encouraging creation of this module.'''

################################################################################

import sys as _sys

################################################################################

def permute(data):
    'Iterate over permutations of data.'
    return _permute(list(data), [])

def permute_list(data):
    'Iterate over list permutations.'
    assert isinstance(data, list), 'Cannot permute non-list.'
    for data in permute(data):
        yield list(data)

def permute_string(data):
    'Iterate over string permutations.'
    assert isinstance(data, str), 'Cannot permute non-string.'
    for data in permute(data):
        yield ''.join(data)

################################################################################

def base8(number):
    'Permute number in base eight.'
    for data in permute(oct(number)[1:]):
        yield int(''.join(data), 8)

def base10(number):
    'Permute number in base ten.'
    for data in permute(str(number)):
        yield int(''.join(data), 10)

def base16(number):
    'Permute number in base sixteen.'
    for data in permute(hex(number)[2:]):
        yield int(''.join(data), 16)

def baseX(number, X):
    'Permute number in specified base.'
    for data in permute(_iter(number, X)):
        yield _int(data, X)

################################################################################

def _permute(items, stack):
    'Private module function.'
    for index in xrange(len(items)):
        stack.append(items.pop(index))
        if items:
            for data in _permute(items, stack):
                yield data
        else:
            yield tuple(stack)
        items.insert(index, stack.pop())
        
def _iter(number, base):
    'Private module function.'
    data = []
    while number:
        data.append(number % base)
        number /= base
    return reversed(data)

def _int(data, base):
    'Private module function.'
    number = 0
    for item in data:
        number *= base
        number += item
    return number

################################################################################

if __name__ == '__main__':
    _sys.stdout.write('Content-Type: text/plain\n\n')
    _sys.stdout.write(file(_sys.argv[0]).read())
