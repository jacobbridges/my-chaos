'''Module for running simple proxies.

This module provides a single class that can build
proxy objects capable of being started and stopped.'''

################################################################################

__version__ = '$Revision: 0 $'
__date__ = 'February 11, 2007'
__author__ = 'Stephen "Zero" Chappell <my.bios@gmail.com>'
__credits__ = '''\
S. Schaub, for introducing me to programming.
S. Sechrest, for writing an introductory tutorial.
S. Leffler, for authoring a more advanced tutorial.'''

################################################################################

import select as _select
import socket as _socket
import sys as _sys
import thread as _thread

################################################################################

class Proxy:

    'Proxy(bind, connect) -> Proxy'
    
    BUFFERSIZE = 2 ** 12

    def __init__(self, bind, connect):
        'Initialize the Proxy object.'
        self.__bind = bind
        self.__connect = connect
        self.__active = False
        self.__thread = False
        self.__lock = _thread.allocate_lock()

    def start(self):
        'Start the Proxy object.'
        self.__lock.acquire()
        self.__active = True
        if not self.__thread:
            self.__thread = True
            _thread.start_new_thread(self.__proxy, ())
        self.__lock.release()

    def stop(self):
        'Stop the Proxy object.'
        self.__lock.acquire()
        self.__active = False
        self.__lock.release()

    def __proxy(self):
        'Private class method.'
        proxy = _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)
        proxy.bind(self.__bind)
        proxy.listen(5)
        while True:
            client = proxy.accept()[0]
            self.__lock.acquire()
            if not self.__active:
                proxy.close()
                client.shutdown(_socket.SHUT_RDWR)
                client.close()
                self.__thread = False
                self.__lock.release()
                break
            self.__lock.release()
            server = _socket.socket(self.FAMILY, self.TYPE)
            server.connect(self.__connect)
            _thread.start_new_thread(self.__serve, (client, server))

    def __serve(self, client, server):
        'Private class method.'
        pairs = {client: server, server: client}
        while pairs:
            for socket in _select.select(pairs.keys(), [], [])[0]:
                string = socket.recv(self.BUFFERSIZE)
                if string:
                    pairs[socket].sendall(string)
                else:
                    pairs[socket].shutdown(_socket.SHUT_WR)
                    socket.shutdown(_socket.SHUT_RD)
                    del pairs[socket]
        client.close()
        server.close()

################################################################################

if __name__ == '__main__':
    _sys.stdout.write('Content-Type: text/plain\n\n')
    _sys.stdout.write(file(_sys.argv[0]).read())
