PORT = 1337

import socket
serv = socket.socket()
serv.bind(('', PORT))
serv.listen(1)
while True:
    data = ''
    recv = ' '
    conn = serv.accept()[0]
    while recv:
        recv = conn.recv(1024)
        if recv:
            data += recv
        else:
            print data
