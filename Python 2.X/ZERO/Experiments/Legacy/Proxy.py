import socket
import sys
import thread

'''EXAMPLE proxy.ini FILE
zcoch215.dorms.bju.edu 3389 3389 <server_name>[white_space]<server_port>[white_space]<proxy_port>[optional_white_space]<optional_text>'''

################################################################################

import Queue; q = Queue.Queue() # TEST

def writer(): # TEST
    while True: sys.stdout.write(q.get())

def write(*args): # TEST
    q.put(' '.join(map(str, args)) + '\n')

def main(setup, error):
    write('PROXY\n=====\n')
    thread.start_new_thread(writer, ()) # TEST
    sys.stderr = file(error, 'a')
    for settings in parse(setup):
        thread.start_new_thread(server, settings)
    lock = thread.allocate_lock()
    lock.acquire()
    lock.acquire()

def parse(setup):
    settings = list()
    for line in file(setup):
        parts = line.split()
        settings.append((parts[0], int(parts[1]), int(parts[2])))
    return settings

def parse(setup): # TEST
    return (('127.0.0.1', 80, 8080), ('127.0.0.1', 8000, 9000))

def server(*settings):
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind(('', settings[2]))
    proxy_socket.listen(5)
    try:
        while True:
            client_socket = proxy_socket.accept()[0]
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.connect((settings[0], settings[1]))
            thread.start_new_thread(forward, (client_socket, server_socket))
            thread.start_new_thread(forward, (server_socket, client_socket))
    finally:
        thread.start_new_thread(server, settings)

def forward(source, destination):
    string = True
    while string:
        string = source.recv(4096)
        if string:
            destination.sendall(string)
        else:
            destination.shutdown(socket.SHUT_WR)
            source.shutdown(socket.SHUT_RD)

def forward(source, destination): # TEST
    string = True
    while string:
        string = source.recv(4096)
        if string:
            destination.sendall(string)
            write('From:', source.getsockname())
            write('To:', destination.getsockname())
            write('Data:', repr(string))
            write()
        else:
            destination.shutdown(socket.SHUT_WR)
            source.shutdown(socket.SHUT_RD)
            write('From:', source.getsockname())
            write('To:', destination.getsockname())
            write('SHUTDOWN')
            write()

################################################################################

if __name__ == '__main__':
    main('proxy.ini', 'error.log')

