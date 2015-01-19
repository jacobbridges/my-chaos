# STD LIBRARY
import sys          # _sys.stdout.write
import thread       # _thread.allocate_lock
import socket       # _socket.socket

# LINK PACKAGE
import pump
import security
import spots

# setup security

security.init('system')

########################################

# 1. "Client" connects to "Server"
# 2. "Client" has "_Client_System" (client.system)
# 3. "client.__getattr__" creates "_Virtual" objects

# 4. "Server" waits for "Client" connections
# 5. "Server" creates "_Remote" objects
# 6. "_Remote" has "_Remote_System" (remote.system)
# 7. "server.__getattr__" creates "_Virtual" objects

'''
* Client
* _Client_System
* _Virtual
* Server
* _Remote
* _Remote_System
'''

########################################

# Clients should just provide the front-end
# call system for talking to the server.

# "Client.system" should provide all of the
# real controls as implemented in another object.

# Follow similar logic on Servers and Remotes.
# Servers have all server-side controls as methods
# while Remote have all client-side controls.

class Client(object):

    # REWRITE - (self, TND, <default_or_security>)
    def __init__(self, title, name, doc, default):
        self.__system = _Client_System(title, name, doc, default)
        self.__lock = thread.allocate_lock()
        self.__timeout = {}

    def __getattr__(self, name):
        pass

    def __call__(self, name, *args, **kwargs):
        pass

    @property
    def system(self):
        return self.__system

    # All of the other code should be in "_Client_System"

########################################

class _Client_System(object):

    def __init__(self, title, name, doc, default):
        self.__TND = pump.TND(title, name, doc)
        self.__security = security.Security(default)
        self.__library = pump.Library()

    # Client controls

    def connect(self, host, port):
        pass

    def disconnect(self):
        pass

    @property
    def TND(self):
        pass

    @property
    def library(self):
        pass

    @property
    def security(self):
        pass

    def timeout(self, seconds):
        pass

    # Server functions

    def get_Title(self):
        pass

    def get_Name(self):
        pass

    def get_Doc(self):
        pass

    def get_List(self):
        pass

    def get_Signature(self, method_name):
        pass

    def get_Doc(self, method_name):
        pass

########################################

class _Virtual(object):
    
    def __getattr__(self, name):
        pass

    def __call__(self, *args, **kwargs):
        pass

########################################
########################################

class Server(object):

    def __init__(self, TND, default, onclient):
        pass

    # Server controls

    def start(self, address port):
        pass

    def stop(self):
        pass

    @property
    def TND(self):
        pass

    @property
    def library(self):
        pass

    @property
    def security(self):
        pass

    def with_client(self, method_name):
        pass

    def without_client(self, method_name):
        pass

########################################

class _Remote(object):

    def __init__(self, server, client, etc):
        pass

    def __getattr__(self, name):
        pass

    def __call__(self, name, *args, **kwargs):
        pass

    @property
    def system(self):
        return self.__system


########################################

class _Remote_System(object):

    def __init__(self, TND, default):
        pass

    # Client functions

    def timeout(self, seconds):
        pass

    def get_Title(self):
        pass

    def get_Name(self):
        pass

    def get_Doc(self):
        pass

    def get_List(self):
        pass

    def get_Signature(self, method_name):
        pass

    def get_Doc(self, method_name):
        pass
