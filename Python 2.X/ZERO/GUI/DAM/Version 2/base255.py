'''Module for string conversion.

This module provides two functions that allow
strings to be encoded and decoded in base 255.'''

__version__ = 1.0

################################################################################

def encode(string, divide=1024):
    'Encode a string to base 255.'
    def encode(string):
        number = int()
        for character in string:
            number *= 257
            number += ord(character) + 1
        string = str()
        while number:
            string = chr(number % 254 + 2) + string
            number /= 254
        return string
    return chr(1).join([encode(string[index:index+divide]) for index in range(0, len(string), divide)])

def decode(string):
    'Decode a string from base 255.'
    def decode(string):
        number = int()
        for character in string:
            number *= 254
            number += ord(character) - 2
        string = str()
        while number:
            string = chr(number % 257 - 1) + string
            number /= 257
        return string
    return str().join([decode(string) for string in string.split(chr(1))])

################################################################################

if __name__ == '__main__':
    import sys
    sys.stdout.write('Content-Type: text/plain\n\n' + file(sys.argv[0]).read())
