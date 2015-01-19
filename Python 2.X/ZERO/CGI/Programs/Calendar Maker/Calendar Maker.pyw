import CGIHTTPServer
import socket
import sys
import thread
import webbrowser

def main():
    try:
        socket.socket().connect(('127.0.0.1', 80))
        webbrowser.open('http://127.0.0.1/htbin/index.py')
    except:
        if len(sys.argv) > 1:
            sys.argv[1] = '80'
        else:
            sys.argv.append('80')
        thread.start_new_thread(CGIHTTPServer.test, ())
        webbrowser.open('http://127.0.0.1/htbin/index.py')
        s = socket.socket()
        s.bind(('', 8080))
        s.listen(1)
        s.accept()

if __name__ == '__main__':
    main()
