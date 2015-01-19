# This should eventually be written as a server that automatically starts
# with the computer. Communication with the server would be handled via
# sockets using a custom protocol. The protocol must be implemented from
# scratch and easy to recreate in any other language. An easy-to-use API
# would be used for writing programs using the registry. NOTE: the API
# and protocol are two different things. The protocol would be based on
# some self-invented standard for moving information across sockets. The
# API, on the other hand, would be the interface provided to programmers
# who wanted to use the registry feature. NOTE: the Python API should be
# a drop-in-replacement for the "_winreg" module. Once completed, "winreg"
# could load either of the modules and probably work on Macintosh and
# Linux. Programs using the winreg module would then be cross-platform
# and not have to worry about working only on Windows.

import bz2
import cPickle

################################################################################

globe = globals()
hives = ('HKEY_CLASSES_ROOT',
         'HKEY_CURRENT_USER',
         'HKEY_LOCAL_MACHINE',
         'HKEY_USERS',
         'HKEY_CURRENT_CONFIG')

for hive in hives:
    try:
        globe[hive] = cPickle.loads(bz2.decompress(file(hive, 'rb').read()))
    except:
        globe[hive] = {}

################################################################################

class HKEYType:

    def __init__(self, handle, path):
        self.path = path
        self.handle = handle
        self.__valid = True

    def Close(self):
        CloseKey(self)
        self.__valid = False
        self.handle = 0

    def Detach(self):
        handle = self.handle
        self.Close()
        return handle

    def __nonzero__(self):
        return self.__valid

    def __eq__(self, other):
        return self.handle == other.handle

    def __ne__(self, other):
        return self.handle != other.handle

    def __int__(self):
        return self.handle

    def __del__(self):
        self.Close()

################################################################################

