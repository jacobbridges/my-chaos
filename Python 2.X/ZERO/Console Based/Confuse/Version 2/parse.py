''' Module for parsing strings of different formats.

This module provides two different functions for parsing
the Bible and for selecting word chunks out of a string.'''

################################################################################

__version__ = '$Revision: 0 $'
__date__ = 'September 22, 2007'
__author__ = 'Stephen "Zero" Chappell <my.bios@gmail.com>'
__credits__ = '''\
H. Chappell, for teaching me the Bible.
J. Pires, for inspiring the word parser.
J. Blanco, for testing the word parser.'''

################################################################################

import sys as _sys

################################################################################

def bible(string):
    'Parse Bible and return 3D array.'
    book = chap = vers = 1
    form = '%02u:%03u:%03u'
    book_s, chap_s, vers_s = [], [], []
    start = 0
    while True:
        try:
            start = string.index(form % (book, chap, vers), start) + 11
            end = string.index('\n\n', start)
            vers_s.append(' '.join(string[start:end].replace('\n', '').split()))
            start = end
            vers += 1
        except:
            if vers != 1:
                chap_s.append(vers_s)
                vers_s = []
                chap += 1
                vers = 1
            elif chap != 1:
                book_s.append(chap_s)
                chap_s = []
                book += 1
                chap = 1
            elif book != 1:
                return book_s
            else:
                raise EOFError

def words(string):
    'Differentiate between words and non-words.'
    data = str(string)
    if data:
        buff = ''
        mode = 'A' <= data[0] <= 'Z' or 'a' <= data[0] <= 'z'
        for char in data:
            if mode == ('A' <= char <= 'Z' or 'a' <= char <= 'z'):
                buff += char
            else:
                yield tuple(buff) if mode else buff
                buff = char
                mode = not mode
        yield tuple(buff) if mode else buff
    else:
        yield data

################################################################################

if __name__ == '__main__':
    _sys.stdout.write('Content-Type: text/plain\n\n')
    _sys.stdout.write(file(_sys.argv[0]).read())
