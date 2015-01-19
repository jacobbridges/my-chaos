SERV = '127.0.0.1'
PORT = 1337

import socket, sys
conn = socket.socket()
conn.connect((SERV, PORT))
sys.stderr = conn.makefile()
