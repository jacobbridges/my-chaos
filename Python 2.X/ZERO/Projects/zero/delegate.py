'''Module for simulating delegated functions.

This module provides access to the Delegate class
that was inspired by the C# programming language.'''

################################################################################

__version__ = '$Revision: 0 $'
__date__ = 'April 17, 2008'
__author__ = 'Stephen "Zero" Chappell <my.bios@gmail.com>'
__credits__ = '''\
S. Schaub, for introducing me to programming.
D. Wooster, for teaching me the C# language.
B. Gates, for the concept of delegates in C#.'''

################################################################################

import sys as _sys

################################################################################

class Delegate:

    'Delegate(function, *args, **kwargs) -> Delegate'
    
    def __init__(self, function, *args, **kwargs):
        'Initialize the Delegate object.'
        self.function = function
        self.args = args
        self.kwargs = kwargs
        
    def __call__(self):
        'Return data from function call.'
        return self.function(*self.args, **self.kwargs)

################################################################################

if __name__ == '__main__':
    _sys.stdout.write('Content-Type: text/plain\n\n')
    _sys.stdout.write(file(_sys.argv[0]).read())
