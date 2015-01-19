from socket import socket, SHUT_RDWR
from getpass import getuser
from os.path import join

from dfs import Release

def main():
    client = socket()
    while True:
        try:
            client.connect((raw_input('Server IP Address? '), 2425))
            break
        except:
            print 'ERROR: Unable To Connect'
    stream = client.makefile('b', 0)
    writer = Release(stream)
    output = join('C:\\Documents and Settings', getuser(), 'My Documents')
    while not writer.EOF():
        writer.release(output)
    stream.close()
    client.shutdown(SHUT_RDWR)
    client.close()

if __name__ == '__main__':
    try:
        main()
        raw_input('\n====\nDONE\n====\n')
    except:
        from traceback import format_exc
        raw_input(format_exc())
