'''Module for Copying & Pasting directories.

This module provides two classes for reading files and
directories into RAM and writing them back out to disk.'''

__version__ = '1.0'

import os as _os
import sys as _sys

################################################################################

class Directory:

    'Directory(path) -> Directory'

    def __init__(self, path):
        'Initialize the Directory object.'
        self.__name = _os.path.basename(path)
        self.__data = []
        for name in _os.listdir(path):
            path_name = _os.path.join(path, name)
            if _os.path.isdir(path_name):
                self.__data.append(Directory(path_name))
            elif _os.path.isfile(path_name):
                self.__data.append(File(path_name))

    def write(self, path):
        'Write directory to path.'
        if self.__name:
            path = _os.path.join(path, self.__name)
            _os.mkdir(path)
        for item in self.__data:
            item.write(path)

################################################################################

class File:

    'File(path) -> File'

    def __init__(self, path):
        'Initialize the File object.'
        self.__name = _os.path.basename(path)
        self.__data = file(path, 'rb').read()

    def write(self, path):
        'Write file to path.'
        file(_os.path.join(path, self.__name), 'wb').write(self.__data)

################################################################################

if __name__ == '__main__':
    _sys.stdout.write('Content-Type: text/plain\n\n')
    _sys.stdout.write(file(_sys.argv[0]).read())
