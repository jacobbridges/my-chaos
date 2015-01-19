ADDRESS = '', 8061  # HOST ADDRESS

import socket
import ImageGrab
import bz2
import struct
import bsdiff
import cPickle

def main():
    client = get_client()
    origin = prime_system(client)
    serve_updates(client, origin)

def get_client():
    server = socket.socket()
    server.bind(ADDRESS)
    server.listen(1)
    client = server.accept()[0]
    server.close()
    return client

def prime_system(client):
    image = ImageGrab.grab()
    width, height = image.size
    origin = image.tostring()
    string = bz2.compress(origin)
    client.sendall(struct.pack('!HHI', width, height, len(string)))
    client.sendall(string)
    return origin

def serve_updates(client, origin):
    while True:
        image = ImageGrab.grab()
        width, height = image.size
        update = image.tostring()
        diff = bsdiff.Diff(origin, update)
        pickle = cPickle.dumps(diff, cPickle.HIGHEST_PROTOCOL)
        string = bz2.compress(pickle)
        client.sendall(struct.pack('!HHI', width, height, len(string)))
        client.sendall(string)
        origin = update
        client.recv(1)

if __name__ == '__main__':
    main()
