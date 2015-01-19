'''Module for automated executions.

This module exposes a Timer class that allows for the scheduled
execution of a function with both arguments and keyword arguments.'''

################################################################################

__version__ = '$Revision: 0 $'
__date__ = 'February 11, 2007'
__author__ = 'Stephen "Zero" Chappell <my.bios@gmail.com>'
__credits__ = '''\
S. Schaub, for introducing me to programming.
D. Wooster, for teaching me the C# language.
B. Gates, for the concept of timers in C#.'''

################################################################################

import sys as _sys
import thread as _thread
import time as _time

################################################################################

class Continuous:

    'Continuous(interval, function, *args, **kwargs) -> Continuous'

    def __init__(self, interval, function, *args, **kwargs):
        'Initialize the Continuous object.'
        self.__interval = interval 
        self.__function = function
        self.__args = args
        self.__kwargs = kwargs
        self.__thread = False
        self.__lock = _thread.allocate_lock()

    def start(self):
        'Start the Continuous object.'
        self.__lock.acquire()
        self.__active = True
        if not self.__thread:
            self.__thread = True
            _thread.start_new_thread(self.__run, ())
        self.__lock.release()

    def stop(self):
        'Stop the Continuous object.'
        self.__lock.acquire()
        self.__active = False
        self.__lock.release()

    def __run(self):
        'Private class method.'
        while True:
            _time.sleep(self.__interval)
            self.__lock.acquire()
            if not self.__active:
                self.__thread = False
                self.__lock.release()
                break
            self.__lock.release()
            self.__function(*self.__args, **self.__kwargs)

################################################################################

class Interruptible:

    'Interruptible(interval, function, *args, **kwargs) -> Interruptible'

    def __init__(self, interval, function, *args, **kwargs):
        'Initialize the Interruptible object.'
        self.__interval = interval 
        self.__function = function
        self.__args = args
        self.__kwargs = kwargs
        self.__active = [False]

    def start(self):
        'Start the Interruptible object.'
        if not self.__active[0]:
            self.__active = [True]
            _thread.start_new_thread(self.__run, (self.__active,))

    def stop(self):
        'Stop the Interruptible object.'
        self.__active[0] = False

    def __run(self, active):
        'Private class method.'
        while True:
            _time.sleep(self.__interval)
            if not active[0]:
                break
            self.__function(*self.__args, **self.__kwargs)

################################################################################

if __name__ == '__main__':
    _sys.stdout.write('Content-Type: text/plain\n\n')
    _sys.stdout.write(file(_sys.argv[0]).read())
