from socket import socket, SHUT_RDWR
from getpass import getuser
from os.path import join
from os import listdir

from dfs import Acquire

def main():
    server = socket()
    server.bind(('', 2425))
    server.listen(1)
    client = server.accept()[0]
    server.close()
    output = client.makefile('b', 0)
    sender = Acquire(output)
    source = join('C:\\Documents and Settings', getuser(), 'My Documents')
    for path in listdir(source):
        sender.acquire(join(source, path))
    output.close()
    client.shutdown(SHUT_RDWR)
    client.close()

if __name__ == '__main__':
    try:
        main()
        raw_input('\n====\nDONE\n====\n')
    except:
        from traceback import format_exc
        raw_input(format_exc())
