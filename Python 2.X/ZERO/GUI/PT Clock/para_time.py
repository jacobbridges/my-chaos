'''Module for Paratessares time conversions.

This module provides several functions that allow
conversion from earth seconds to Paratessares time units.'''

################################################################################

__version__ = '$Revision: 0 $'
__date__ = 'April 17, 2008'
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

EPOCH_CORRECTION = 946684800
MICREV_PER_DAY = 1000000
MILREV_PER_DAY = 1000
DAYS_PER_WEEK = 7
WEEKS_PER_MONTH = 4
MONTHS_PER_SEASON = 3
SEASONS_PER_YEAR = 4
SECONDS_PER_DAY = 86400
SECONDS_PER_WEEK = SECONDS_PER_DAY * DAYS_PER_WEEK
SECONDS_PER_MONTH = SECONDS_PER_WEEK * WEEKS_PER_MONTH
SECONDS_PER_SEASON = SECONDS_PER_MONTH * MONTHS_PER_SEASON
SECONDS_PER_YEAR = SECONDS_PER_SEASON * SEASONS_PER_YEAR

################################################################################

def seconds():
    'Return seconds since the epoch.'
    return _time.time() - EPOCH_CORRECTION

def micrev(seconds):
    'Convert from seconds to mille.'
    return int(seconds % SECONDS_PER_DAY * MICREV_PER_DAY / SECONDS_PER_DAY % MILREV_PER_DAY)

def milrev(seconds):
    'Convert from seconds to khilioi.'
    return int(seconds % SECONDS_PER_DAY * MILREV_PER_DAY / SECONDS_PER_DAY)

def day(seconds):
    'Convert from seconds to day.'
    return int(seconds) / SECONDS_PER_DAY % DAYS_PER_WEEK

def week(seconds):
    'Convert from seconds to week.'
    return int(seconds) / SECONDS_PER_WEEK % WEEKS_PER_MONTH

def month(seconds):
    'Convert from seconds to month.'
    return int(seconds) / SECONDS_PER_MONTH % MONTHS_PER_SEASON

def season(seconds):
    'Convert from seconds to season.'
    return int(seconds) / SECONDS_PER_SEASON % SEASONS_PER_YEAR

def year(seconds):
    'Convert from seconds to year.'
    return int(seconds) / SECONDS_PER_YEAR

################################################################################

UNITS = year, season, month, week, day, milrev, micrev

def format(seconds, format='%u.%u.%u.%u.%u.%03u.%03u', units=UNITS):
    'Convert from seconds to string.'
    return format % tuple(function(seconds) for function in units)

################################################################################

class Micrev_Timer:

    'Micrev_Timer(function, *args, **kwargs) -> Micrev_Timer'

    def __init__(self, function, *args, **kwargs):
        'Initialize the Micrev_Timer object.'
        self.__function = function
        self.__args = args
        self.__kwargs = kwargs
        self.__thread = False
        self.__lock = _thread.allocate_lock()

    def start(self):
        'Start the Micrev_Timer object.'
        self.__lock.acquire()
        self.__active = True
        if not self.__thread:
            self.__thread = True
            _thread.start_new_thread(self.__run, ())
        self.__lock.release()

    def stop(self):
        'Stop the Micrev_Timer object.'
        self.__lock.acquire()
        self.__active = False
        self.__lock.release()

    def __run(self):
        'Private class method.'
        start, next = _time.clock(), 0
        while True:
            next += 1
            sleep = start + next * 0.0864 - _time.clock()
            assert sleep >= 0, 'Function Was Too Slow'
            _time.sleep(sleep)
            self.__lock.acquire()
            if not self.__active:
                self.__thread = False
                self.__lock.release()
                break
            self.__lock.release()
            self.__function(*self.__args, **self.__kwargs)

################################################################################

class Quantum_Timer:

    'Quantum_Timer(function, *args, **kwargs) -> Quantum_Timer'

    def __init__(self, function, *args, **kwargs):
        'Initialize the Quantum_Timer object.'
        self.__function = function
        self.__args = args
        self.__kwargs = kwargs
        self.__thread = False
        self.__lock = _thread.allocate_lock()

    def start(self):
        'Start the Quantum_Timer object.'
        self.__lock.acquire()
        self.__active = True
        if not self.__thread:
            self.__thread = True
            _thread.start_new_thread(self.__run, ())
        self.__lock.release()

    def stop(self):
        'Stop the Quantum_Timer object.'
        self.__lock.acquire()
        self.__active = False
        self.__lock.release()

    def __run(self):
        'Private class method.'
        while True:
            time = _time.clock()        # BETA TIMING CODE
            next = time + 0.0864        # BETA TIMING CODE
            over = next % 0.0864        # BETA TIMING CODE
            diff = next - time - over   # BETA TIMING CODE
            _time.sleep(diff)           # BETA TIMING CODE
            self.__lock.acquire()
            if not self.__active:
                self.__thread = False
                self.__lock.release()
                break
            self.__lock.release()
            self.__function(*self.__args, **self.__kwargs)

################################################################################

if __name__ == '__main__':
    _sys.stdout.write('Content-Type: text/plain\n\n')
    _sys.stdout.write(file(_sys.argv[0]).read())
