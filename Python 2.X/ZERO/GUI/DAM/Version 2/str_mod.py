'''Module for modifying strings.

This module provides several functions for creating named tables,
translating strings in both directions, and partitioning strings.'''

__version__ = 1.0

################################################################################

import random

def table(name=None):
    'Create a table suitable for translation.'
    random.seed(name)
    return str().join(map(chr, random.sample(range(256), 256)))

def translate(string, table, direction):
    'Translate a string in the direction specified.'
    if direction:
        table = str().join(dict([(ord(c), chr(i)) for i, c in enumerate(table)]).values())
    return string.translate(table)

def partition(string, size):
    'Partition a string into substrings.'
    return (string[index:index+size] for index in range(0, len(string), size))

def qualify(table):
    'Return the quality of a table.'
    master = str().join(map(chr, range(256)))
    slave, Q = master.translate(table), 0
    while slave != master:
        slave = slave.translate(table)
        Q += 1
    return Q

################################################################################

if __name__ == '__main__':
    import sys
    sys.stdout.write('Content-Type: text/plain\n\n' + file(sys.argv[0]).read())
