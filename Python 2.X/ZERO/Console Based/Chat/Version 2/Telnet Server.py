import socket
import select
import sys

################################################################################

class Telnet_Server:

    def __init__(self, port=23):
        self.server = socket.socket()
        self.server.bind(('', port))
        self.server.listen(5)
        self.socket = [self.server]
        sys.stdout.write('Telnet Server started on port %s' % port)

    def run(self):
        while True:
            for socket in select.select(self.socket, (), ())[0]:
                if socket is self.server:
                    self.accept()
                else:
                    string = socket.recv(4096)
                    if string:
                        self.broadcast(socket, string)
                    else:
                        string = '\r\nEXIT:  %s:%s\r\n' % socket.getpeername()
                        self.broadcast(socket, string)
                        socket.close()
                        self.socket.remove(socket)

    def accept(self):
        socket, peername = self.server.accept()
        self.socket.append(socket)
        socket.sendall('You\'re connected to the Python telnet server\r\n')
        self.broadcast(socket, '\r\nENTER: %s:%s\r\n' % peername)

    def broadcast(self, omit, string):
        for socket in self.socket:
            if socket not in (self.server, omit):
                socket.sendall(string)
        sys.stdout.write(string)

################################################################################

if __name__ == '__main__':
    Telnet_Server().run()
