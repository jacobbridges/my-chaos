# Name & Description
# ==================

'''Support module for use by CGI scripts.

This module provides several functions and variables
that help with printing text and accessing form data.'''

# Data & Imports
# ==============

__all__ = ['execute', 'print_html', 'print_plain', 'print_self',
           'dictionary', 'string']
__version__ = '1.2'

import os
import sys
import types

# Public Names
# ============

def execute(main, exception):
    '''execute(function main, str exception)

    Execute main unless exception.'''
    assert_type((types.FunctionType, main), (str, exception))
    if exception == string:
        print_self()
    else:
        main()

def print_html(text):
    '''print_html(str text)

    Print text as HTML.'''
    assert_type((str, text))
    print 'Content-Type: text/html'
    print
    print text
    sys.exit(0)

def print_plain(text):
    '''print_plain(str text)

    Print text as plain.'''
    assert_type((str, text))
    print 'Content-Type: text/plain'
    print
    print text
    sys.exit(0)

def print_self():
    '''print_self()

    Print __main__ as plain.'''
    print 'Content-Type: text/plain'
    print
    print file(sys.argv[0]).read()
    sys.exit(0)

# Private Names
# =============

def export():
    global dictionary, string
    dictionary = string = None
    try:
        string = os.environ['QUERY_STRING']
        temp = string.replace('+', ' ').split('&')
        for index in range(len(temp)):
            temp[index] = temp[index].split('=')
        dictionary = dict()
        for parameter, value in temp:
            dictionary[decode(parameter)] = decode(value)
    except:
        pass

def decode(string):
    assert_type((str, string))
    index = string.find('%')
    while index != -1:
        string = string[:index] + chr(int(string[index+1:index+3], 16)) + string[index+3:]
        index = string.find('%', index + 1)
    return string

def assert_type(*tuples):
    for types, objects in tuples:
        if type(objects) is not types:
            raise TypeError

# Execute Conditional
# ===================

if __name__ == '__main__':
    print_self()
else:
    export()
