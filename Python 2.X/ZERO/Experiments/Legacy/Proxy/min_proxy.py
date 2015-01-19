from socket import *
from time import *

# SECTION - DONE

################################################################################

class RoundRobin:

    def __init__(self):
        self.__pointer = int()
        self.__ring = list()

    def __len__(self):
        return len(self.__ring)

    def add(self, item):
        self.__ring.insert(self.__pointer, item)
        self.__pointer += 1

    def next(self):
        self.__pointer = (self.__pointer + 1) % len(self.__ring)
        return self.__ring[self.__pointer]

    def remove(self):
        del self.__ring[self.__pointer]
        self.__pointer -= 1

# SECTION - DEBUG
# In "remove," the pointer can become negative.

################################################################################

class Delegate:
    
    def __init__(self, target, *args, **kwargs):
        self.__target = target
        self.__args = args
        self.__kwargs = kwargs
        
    def __call__(self, *args, **kwargs):
        if args or kwargs:
            return self.__target(*args, **kwargs)
        else:
            return self.__target(*self.__args, **self.__kwargs)
        
    def args(self, *args):
        self.__args = args
        return self
        
    def kwargs(self, **kwargs):
        self.__kwargs = kwargs
        return self

# SECTION - DONE

################################################################################

class PumpState:
    
    def __init__(self, timeout):
        self.error = False
        self.timeout = timeout
        self.last_action = time()
        self.active = True
        self.reading = True
        self.buffer = ''

# SECTION - IN PROCESS

# THEORY (DESIGN)

# /----------------\  /--------------------\  /------------------\
# | pump to server |--| reading state flag |--| alive state flag |--\
# \----------------/  | buffer for reading |  | last action time |  |
#                     \--------------------/  | error state flag |  |  /---------------\
#                                             \------------------/  |--| timeout value |
#                                                                   |  | shutdown flag |
# /----------------\  /--------------------\  /------------------\  |  \---------------/
# | pump to client |--| reading state flag |--| alive state flag |--/
# \----------------/  | buffer for reading |  | last action time |
#                     \--------------------/  | error state flag |
#                                             \------------------/

################################################################################

def main(setup, timeout):
    delegates = RoundRobin()
    for settings in parse(setup):
        start_new_server(timeout, delegates, settings)
    # START DEBUG
    import os
    def debug(delegates):
        os.system('cls')
        print 'workers =', len(delegates) - 1
    delegates.add(Delegate(debug, delegates))
    # END DEBUG
    while True:
        if delegates.next()():
            delegates.remove()

def parse(setup):
    settings = list()
    for line in file(setup):
        parts = line.split()
        settings.append((parts[0], int(parts[1]), int(parts[2])))
    return settings

def start_new_server(timeout, delegates, settings):
    dock_socket = socket()
    dock_socket.bind(('', settings[2]))
    dock_socket.listen(5)
    dock_socket.setblocking(False)
    delegates.add(Delegate(server, timeout, delegates, \
                           settings[:-1], dock_socket))

# SECTION - DONE

################################################################################

def server(timeout, delegates, settings, dock_socket):
    try:
        while True:
            client_socket = dock_socket.accept()[0]
            client_socket.setblocking(False)
            server_socket = socket()
            server_socket.connect(settings)
            server_socket.setblocking(False)
            share = PumpShare(timeout)
            delegates.add(Delegate(forward, client_socket, server_socket, share, PumpState()))
            delegates.add(Delegate(forward, server_socket, client_socket, share, PumpState()))
    except:
        pass

def forward(source, destination, state, share): # Cleanup work done with share.
    if share.shutdown:
        if state.reading:
            source.shutdown(SHUT_RD)
        destination.shutdown(SHUT_WR)
        source.close()
        destination.close()
        return True
    pump(source, destination, state) # Has been checked.
    if not state.reading and not state.buffer:
        destination.shutdown(SHUT_WR)
        share.alone = True
        return True
    if check and share.last_action > share.timeout:
        if share.failing or share.alone:
            share.shutdown = True
            if state.reading:
                source.shutdown(SHUT_RD)
            destination.shutdown(SHUT_WR)
            return True
        share.failing = True

def pump(source, destination, state): # I like it. :)
    if state.reading:
        try:
            string = source.recv(4096)
            if string:
                state.buffer += string
            else:
                source.shutdown(SHUT_RD)
                state.reading = False
        except:
            pass
    if state.buffer:
        try:
            sent = destination.send(state.buffer)
            if sent:
                state.buffer = state.buffer[sent:]
                return True
        except:
            pass
    return False

# SECTION - UNCHECKED

################################################################################

if __name__ == '__main__':
    main('proxy.ini', 1)

# SECTION - DONE
