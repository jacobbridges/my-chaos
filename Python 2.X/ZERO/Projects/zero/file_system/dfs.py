'''Module for Directory and File Serialization.

This module provides two classes that implement the
DFS (Directory and File Serialization) file format.'''

################################################################################

__version__ = '$Revision: 0 $'
__date__ = 'April 17, 2008'
__author__ = 'Stephen "Zero" Chappell <my.bios@gmail.com>'
__credits__ = '''\
S. Schaub, for introducing me to programming.
G. Niemeyer, for authoring with the bz2 module.
R. Townsend, for helping with the tarfile module.'''

################################################################################

import os as _os
import sys as _sys

################################################################################

FORMAT_DOCUMENTATION = '''\
Directory
    Header
        0,aaa,b,c,dd
            0 = Directory
            a = Pointer Size (bytes)
            b = Name Size (bytes)
            c = Content Flag
            d = Type Code
                00 = End
                01 = Error
                10 = Error
                11 = Real
    Pointer
    Name Size
    Name

File
    Header
        1,aaa,b,ccc
            1 = File
            a = Pointer Size (bytes)
            b = Name Size (bytes)
            c = Data Size (bytes)
    Pointer
    Name Size
    Name
    Data Size
    Data'''

################################################################################

class Acquire:

    'Acquire(destination) -> Acquire'

    BUFF_SIZE = 2 ** 20

    def __init__(self, destination):
        'Initialize the Acquire object.'
        self.__destination = destination
        if hasattr(destination, 'name'):
            self.__destination_path = _os.path.abspath(destination.name)
        else:
            self.__destination_path = None
        self.__archive = False

    def acquire(self, source):
        'Save source to destination.'
        source = _os.path.abspath(source)
        self.__pointer = 0
        if self.__archive:
            self.__destination.write('\0')
        else:
            self.__archive = True
        if _os.path.isdir(source):
            self.__dir(source, '\0')
        elif _os.path.isfile(source):
            if source == self.__destination_path:
                raise ValueError('Source cannot be destination.')
            self.__file(source, '\0')
        else:
            raise ValueError('Source must be directory or file.')

    def __dir(self, source, pointer):
        'Private class method.'
        name = _os.path.basename(source)
        name_size = _str(len(name))
        try:
            dir_list = _os.listdir(source)
        except:
            dir_list = ()
        a = len(pointer) - 1 << 4
        b = len(name_size) - 1 << 3
        if dir_list:
            self.__pointer += 1
            cd = 7
        else:
            cd = 3
        header = chr(a + b + cd)
        self.__destination.write(header + pointer + name_size + name)
        pointer = _str(self.__pointer)
        for name in dir_list:
            source_name = _os.path.join(source, name)
            if source_name == self.__destination_path:
                continue
            elif _os.path.isdir(source_name):
                self.__dir(source_name, pointer)
            elif _os.path.isfile(source_name):
                self.__file(source_name, pointer)

    def __file(self, source, pointer):
        'Private class method.'
        name = _os.path.basename(source)
        name_size = _str(len(name))
        try:
            source = open(source, 'rb')
            source.seek(0, 2)
            data_size = _str(source.tell())
            source.seek(0, 0)
        except:
            source = None
            data_size = '\0'
        a = len(pointer) - 1 << 4
        b = len(name_size) - 1 << 3
        c = len(data_size)
        header = chr(127 + a + b + c)
        self.__destination.write(header + pointer + name_size + name)
        self.__destination.write(data_size)
        if source:
            data_size = _int(data_size)
            try:
                while data_size:
                    buff = source.read(min(self.BUFF_SIZE, data_size))
                    if buff:
                        self.__destination.write(buff)
                        data_size -= len(buff)
                    else:
                        raise IOError('File changed size while open.')
                position = source.tell()
                source.seek(0, 2)
                if position != source.tell():
                    raise IOError('File changed size while open.')
            finally:
                source.close()

################################################################################

class Release:

    'Release(source) -> Release'

    BUFF_SIZE = 2 ** 20

    def __init__(self, source):
        'Initialize the Release object.'
        self.__source = source
        self.__EOF = False

    def release(self, destination):
        'Save source to destination.'
        if self.__EOF:
            raise EOFError('End Of File Found')
        self.__parents = [_os.path.abspath(destination)]
        header = self.__source.read(1)
        header = ord(header) if header else -1
        if header == -1:
            self.__EOF = True
            raise Warning('Irregular File Termination Detected')
        while header != -1 and (header > 127 or header & 3):
            if header < 128:
                if header & 3 != 3:
                    raise IOError('Corrupt Directory Header Found')
                self.__dir(header)
            else:
                self.__file(header)
            header = self.__source.read(1)
            header = ord(header) if header else -1
        if header == -1:
            self.__EOF = True

    def EOF(self):
        'Return the End Of File status.'
        return self.__EOF

    def __dir(self, header):
        'Private class method.'
        parent = self.__parents[_int(self.__read((header >> 4 & 7) + 1))]
        name = self.__read(_int(self.__read((header >> 3 & 1) + 1)))
        path = _os.path.join(parent, name)
        if _os.path.exists(path):
            if _os.path.isfile(path):
                raise IOError('Path Already Exists')
        else:
            _os.mkdir(path)
        if header >> 2 & 1:
            self.__parents.append(path)

    def __file(self, header):
        'Private class method.'
        parent = self.__parents[_int(self.__read((header >> 4 & 7) + 1))]
        name = self.__read(_int(self.__read((header >> 3 & 1) + 1)))
        destination = open(_os.path.join(parent, name), 'wb')
        data_size = _int(self.__read((header & 7) + 1))
        try:
            while data_size:
                buff = self.__source.read(min(self.BUFF_SIZE, data_size))
                if buff:
                    destination.write(buff)
                    data_size -= len(buff)
                else:
                    raise IOError('End Of File Found')
        finally:
            destination.close()

    def __read(self, size):
        'Private class method.'
        if size:
            buff = ''
            while size:
                temp = self.__source.read(size)
                if temp:
                    buff += temp
                    size -= len(temp)
                else:
                    raise IOError('End Of File Found')
            return buff
        raise IOError('Zero Length String Found')

################################################################################

def _str(integer):
    'Private module function.'
    if integer:
        string = ''
        while integer:
            string = chr(integer & 0xFF) + string
            integer >>= 8
        return string
    return '\0'

def _int(string):
    'Private module function.'
    integer = 0
    for c in string:
        integer <<= 8
        integer += ord(c)
    return integer

################################################################################

if __name__ == '__main__':
    _sys.stdout.write('Content-Type: text/plain\n\n')
    _sys.stdout.write(file(_sys.argv[0]).read())
