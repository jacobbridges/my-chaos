import socket
import spots
import pump
import security

def main():
    # Build a QRI object with chatter-box.
    sock = socket.socket()
    sock.bind(('', 2100))
    sock.listen(5)
    sock2 = sock.accept()[0]
    QRI = spots.qri(sock2)
    # Build a TNB object with dummy data.
    doc = '''\
This is a test server used to test the
concepts already put forth. Since it has
been a while since "Link" has been in
development, this server is being written
as a test course to verify what is already
in place for finishing the library.'''
    TND = pump.TND('TEST', 'BTiger', doc)
    # Build and populate a library object.
    security.init() # Must be initialized for Library.
    library = pump.Library()
    import random
    library['random'] = random.Random()
    import string
    library['string'] = string
    # The pump needs security.
    sec_obj = security.Security(True)
    # Create a universal callback function.
    def callme(name, *args, **kwargs):
        print '''
%s was called with:

Args = %r

Kwargs = %r

%s''' % (name, args, kwargs, '=' * 80)
    import functools
    onquit = functools.partial(callme, 'OnQuit')
    onexit = functools.partial(callme, 'OnExit')
    onerror = functools.partial(callme, 'OnError')
    # Hope that the pump actually works.
    test_pump = pump.Pump(QRI, TND, library, sec_obj,
                          onquit, onexit, onerror)
    import thread
    lock = thread.allocate_lock()
    print 'Now we wait, listen, and hope this works.'
    lock.acquire()
    # ... add a few more objects to the library first.
    library['TND'] = TND
    library['library'] = library
    library['security'] = sec_obj
    library['pump'] = test_pump
    library['unlock'] = lock.release
    lock.acquire()

if __name__ == '__main__':
    main()
