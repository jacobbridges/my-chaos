import os
import Queue
import socket
import sys
import thread
import threading

MAIN_PORT = 22557

################################################################################

class sys_com(threading.Thread):

    def __init__(self, target, *args):
        threading.Thread.__init__(self)
        self.__target = target
        self.__args = args
        self.__status = None

    def run(self):
        self.__status = os.system(' '.join([self.__target] + [str(item) for item in self.__args]))

    def status(self):
        return self.__status

################################################################################

class aux_win:

    def __init__(self):
        self.__off = False
        self.__queue = Queue.Queue()
        thread.start_new_thread(self.__run, ())

    def close(self):
        self.__off = True
        thread.start_new_thread(self.__send, ('0',))

    def write(self, data):
        self.__queue.put(str(data))

    def clear(self):
        thread.start_new_thread(self.__send, ('1',))

    def __send(self, string):
        temp = socket.socket()
        temp.connect(('127.0.0.1', self.__port))
        temp.sendall(string)
        temp.shutdown(socket.SHUT_RDWR)
        temp.close()

    def __run(self):
        self.__server = socket.socket()
        #port = 1000
        #while True:
        #    try:
        #        self.__server.bind(('', port))
        #        break
        #    except:
        #        port += 1
        self.__server.bind(('', MAIN_PORT))
        self.__server.listen(1)
        thread.start_new_thread(self.__run_server, ())
        #self.__sys_com = sys_com('window.py', port)
        #self.__sys_com.start()
        os.startfile('window.py')

    def __run_server(self):
        temp = self.__server
        self.__server = self.__server.accept()[0]
        # temp.shutdown(socket.SHUT_RDWR)
        temp.close()
        self.__set_port()
        while True:
            try:
                string = self.__queue.get(True, 1)
            except:
                if self.__off:
                    self.__server.shutdown(socket.SHUT_WR)
                    self.__server.close()
                    break
                else:
                    continue
            self.__server.sendall(string)

    def __set_port(self):
        string = ''
        while True:
            string += self.__server.recv(1024)
            if '\x00' in string:
                string = string[:string.index('\x00')]
                self.__port = int(string)
                self.__server.shutdown(socket.SHUT_RD)
                break
            
################################################################################

def main():
    server = socket.socket()
    port = 1001
    while True:
        try:
            server.bind(('', port))
            break
        except:
            port += 1
    server.listen(1)
    run = [True]
    thread.start_new_thread(client, (port, run))
    while True:
        temp = server.accept()[0]
        string = temp.recv(1024)
        if string[0] == '1':
            if os.name == 'nt':
                os.system('cls')
            elif os.name == 'posix':
                os.system('clear')
        elif string[0] == '0':
            run[0] = False
            break
    #server.shutdown(socket.SHUT_RDWR)
    server.close()
    
def client(port, run):
    sock = socket.socket()
    #sock.connect(('127.0.0.1', int(sys.argv[1])))
    sock.connect(('127.0.0.1', MAIN_PORT))
    sock.sendall(str(port) + '\x00')
    sock.shutdown(socket.SHUT_WR)
    sock.setblocking(True)
    sock.settimeout(1)
    while True:
        try:
            string = sock.recv(1024)
        except:
            if run[0]:
                continue
            else:
                break
        if string:
            sys.stdout.write(string)
        else:
            break
    sock.shutdown(socket.SHUT_RD)
    sock.close()

################################################################################

if __name__ == '__main__':
    main()
