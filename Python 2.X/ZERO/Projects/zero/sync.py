'''Module for syncronizing mutliple threads.

This module provides access to the Sync class which
can help to automatically syncronize several threads.'''

################################################################################

__version__ = '$Revision: 0 $'
__date__ = 'February 11, 2007'
__author__ = 'Stephen "Zero" Chappell <my.bios@gmail.com>'
__credits__ = '''\
S. Schaub, for introducing me to programming.
G. Rossum, for allowing thread support in Python.
B. Gates, for another OS on which Python runs.'''

################################################################################

import sys as _sys
import thread as _thread

################################################################################

class Sync:

    'Sync(threads) -> Sync'

    def __init__(self, threads):
        'Initialize the Sync object.'
        self.__threads = threads
        self.__count = 0
        self.__main = _thread.allocate_lock()
        self.__exit = _thread.allocate_lock()
        self.__exit.acquire()

    def sync(self):
        'Automatically synchronize calling threads.'
        self.__main.acquire()
        self.__count += 1
        if self.__count < self.__threads:
            self.__main.release()
        else:
            self.__exit.release()
        self.__exit.acquire()
        self.__count -= 1
        if self.__count > 0:
            self.__exit.release()
        else:
            self.__main.release()

################################################################################

if __name__ == '__main__':
    _sys.stdout.write('Content-Type: text/plain\n\n')
    _sys.stdout.write(file(_sys.argv[0]).read())
