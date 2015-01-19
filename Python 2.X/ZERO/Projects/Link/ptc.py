import socket
import spots

sock = socket.socket()
sock.connect(('localhost', 2100))
QRI = spots.qri(sock)

def call(mode, name, *args, **kwargs):
    mode, data = QRI.call((mode, name, args, kwargs), 1)
    if mode:
        return data
    raise data
