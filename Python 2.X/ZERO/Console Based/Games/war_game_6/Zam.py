# Name & Description
# ==================

'''Support module for array and matrix use.

This module provides two classes that emulate one and two
dimentional lists with fixed sizes but mutable internals.'''

# Data & Imports
# ==============

__all__ = ['array', 'matrix']
__version__ = '1.1'

import sys

# Public Names
# ============

class array(object):

    '''array(length) -> new array
    array(length, value) -> initialized from value'''

    def __init__(self, length, value=None):
        '''x.__init__(...) initializes x'''
        self.__data = range(length)
        for index in range(length):
            self.__data[index] = value

    def __repr__(self):
        '''x.__repr__() <==> repr(x)'''
        return repr(self.__data)

    def __len__(self):
        '''x.__len__() <==> len(x)'''
        return len(self.__data)

    def __getitem__(self, key):
        '''x.__getitem__(y) <==> x[y]'''
        return self.__data[key]

    def __setitem__(self, key, value):
        '''x.__setitem__(i, y) <==> x[i]=y'''
        self.__data[key] = value

    def __delitem__(self, key):
        '''x.__delitem__(y) <==> del x[y]'''
        self.__data[key] = None

    def __iter__(self):
        '''x.__iter__() <==> iter(x)'''
        return iter(self.__data)

    def __contains__(self, value):
        '''x.__contains__(y) <==> y in x'''
        return value in self.__data

class matrix(object):

    '''matrix(rows, columns) -> new matrix
    matrix(rows, columns, value) -> initialized from value'''

    def __init__(self, rows, columns, value=None):
        '''x.__init__(...) initializes x'''
        self.__data = array(rows)
        for index in range(rows):
            self.__data[index] = array(columns, value)

    def __repr__(self):
        '''x.__repr__() <==> repr(x)'''
        return repr(self.__data)

    def __len__(self):
        '''x.__len__() <==> len(x)'''
        return len(self.__data)

    def __getitem__(self, key):
        '''x.__getitem__(y) <==> x[y]'''
        return self.__data[key]

    def __setitem__(self, key, value):
        '''x.__setitem__(i, y) <==> x[i]=y'''
        self.__data[key] = array(len(self.__data[key]), value)

    def __delitem__(self, key):
        '''x.__delitem__(y) <==> del x[y]'''
        self.__data[key] = array(len(self.__data[key]))

    def __iter__(self):
        '''x.__iter__() <==> iter(x)'''
        return iter(self.__data)

    def __contains__(self, value):
        '''x.__contains__(y) <==> y in x'''
        for item in self.__data:
            if value in item:
                return True
        return False

# Private Names
# =============

def main():
    print 'Content-Type: text/plain'
    print
    print file(sys.argv[0]).read()

# Execute Main
# ============

if __name__ == '__main__':
    main()
