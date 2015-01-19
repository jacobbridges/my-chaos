import ImageGrab
import socket
import struct
import zlib

def main():
    server = socket.socket()
    server.bind(('', 8060))
    server.listen(1)
    client = server.accept()[0]
    while True:
        image = ImageGrab.grab()
        width, height = image.size
        string = zlib.compress(image.tostring())
        client.sendall(struct.pack('!HHI', width, height, len(string)))
        client.sendall(string)
        client.recv(1)

if __name__ == '__main__':
    main()
