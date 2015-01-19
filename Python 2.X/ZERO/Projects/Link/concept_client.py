class Virtual:

    'Virtual(connection, name) -> Virtual'
    
    def __init__(self, link, name):
        'Initialize the Virtual object.'
        self.__link = link
        self.__name = name

    def __getattr__(self, name):
        'Extend the object call.'
        return Virtual(self.__link, '%s.%s' % (self.__name, name))

    def __call__(self, *args, **kwargs):
        'Call the object specified.'
        return self.__link(self.__name, *args, **kwargs)

################################################################################

class Client:

    'Client() -> Client'

    def __init__(self):
        'Initialize the Client object.'
        self.__client() # create client controls
        self.__server() # create server controls
        self.__active = False
        self.__thread = False
        self.__lock = thread.allocate_lock()
        # self.__socket
        # self.__qri
        self.__title = None         # client's title
        self.__name = None          # client's name
        self.__documentation = None # client's documentation
        self.__objects = {}         # installed objects
        # attributes for timeout control
        self.__thread_timeout = {}
        self.__tt_lock = thread.allocate_lock()
        # processor control switch
        self.__syncronized = False
        self.__sync_lock = thread.allocate_lock()

    def __client(self):
        'Create client controls.'
        class client: pass
        client = client()
        # connection controls
        client.connect = self.__client_connect
        client.disconnect = self.__client_disconnect
        # documentation controls
        client.title = self.__client_title
        client.name = self.__client_name
        client.documentation = self.__client_documentation
        # object controls
        client.install = self.__client_install
        client.uninstall = self.__client_uninstall
        # timeout controls
        client.timeout = self.__client_timeout
        client.clear = self.__client_clear
        # syncronization control
        client.syncronize = self.__client_syncronize
        # publish client controls
        self.client = client

    def __server(self):
        'Create server controls.'
        class server: pass
        server = server()
        # documentation controls
        server.title = self.__server_title
        server.name = self.__server_name
        server.documentation = self.__server_documentation
        # object controls
        server.objects = self.__server_objects
        server.signature = self.__server_signature
        server.help = self.__server_help
        # publish server controls
        self.server = server

    # CLIENT CONTROL METHODS

    def __client_connect(self, host, port):
        'Connect client to specified address.'
        assert not self.__active, 'Client Is Active'
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((host, port))
        self.__qri = spots.qri(self.__socket)
        # START SERVER CODE
        self.__lock.acquire()
        if not self.__thread:
            self.__thread = True
            thread.start_new_thread(self.__processor, ())
        self.__lock.release()
        # END SERVER CODE
        self.__active = True

    def __client_disconnect(self):
        'Disconnect client from server.'
        assert self.__active, 'Client Is Not Active'
        self.__active = False
        self.__socket.shutdown(socket.SHUT_RDWR)
        self.__socket.close()
        del self.__socket, self.__qri

    def __client_title(self, title):
        'Set the client\'s title.'
        self.__title = str(title)

    def __client_name(self, name):
        'Set the client\'s name.'
        self.__name = str(name)

    def __client_documentation(self, documentation):
        'Set the client\'s documentation.'
        self.__documentation = str(documentation)

    def __client_install(self, name, obj):
        'Install an object.'
        check_name(name)
        self.__objects[str(name)] = obj

    def __client_uninstall(self, name):
        'Uninstall an object.'
        check_name(name)
        del self.__objects[str(name)]

    def __client_timeout(self, seconds):
        'Set this thread\'s timeout for calls.'
        if not isinstance(seconds, (float, int, long)):
            raise TypeError, 'timeout must be of type float, int, or long'
        if not seconds >= 0:
            raise ValueError, 'timeout must be greater than or equal to 0'
        self.__tt_lock.acquire()
        self.__thread_timeout[thread.get_ident()] = seconds
        self.__tt_lock.release()

    def __client_clear(self):
        'Clear timeouts for this thread.'
        ident = thread.get_ident()
        self.__tt_lock.acquire()
        if self.__thread_timeout.has_key(ident):
            del self.__thread_timeout[ident]
        self.__tt_lock.release()

    # SERVER CONTROL METHODS

    def __server_title(self):
        'Get the server\'s title.'
        return self.__call(False, 'title')

    def __server_name(self):
        'Get the server\'s name.'
        return self.__call(False, 'name')

    def __server_documentation(self):
        'Get the server\'s documentation.'
        return self.__call(False, 'documentation')

    def __server_objects(self):
        'List the objects on the server.'
        return self.__call(False, 'objects')

    def __server_signature(self, name):
        'Get an object\'s signature.'
        return self.__call(False, 'signature', name)

    def __server_help(self, name):
        'Get an object\'s documentation.'
        return self.__call(False, 'help', name)

    # ROX INTERFACE

    def __getattr__(self, name):
        'Get a virtual, callable object.'
        return Virtual(self, name)

    def __call__(self, name, *args, **kwargs):
        'Allow call of object.'
        return self.__call(True, name, args, kwargs)

    # PRIVATE CLASS METHODS

    def __call(self, *obj):
        'Make a call and handle errors.'
        assert self.__active, 'Client Is Not Active'
        ident = thread.get_ident()
        self.__tt_lock.acquire()
        if self.__thread_timeout.has_key(ident):
            timeout = self.__thread_timeout[ident]
            self.__tt_lock.release()
            no_error, data = self.__qri.call(obj, timeout)
        else:
            self.__tt_lock.release()
            no_error, data = self.__qri.call(obj)
        if no_error:
            return data
        raise data

    def __processor(self):
        'Dispatch queries to worker threads.'
        while True:
            try:
                ID, obj = self.__qri.query(5)
                #ID, obj = self.__qri.query()    # TEST
                self.__sync_lock.acquire()
                sync = self.__syncronized
                self.__sync_lock.release()
                if sync:
                    self.__worker(ID, obj)
                else:
                    thread.start_new_thread(self.__worker, (ID, obj))
            except Warning:
                pass
            except:
                self.__lock.acquire()
                self.__thread = False
                # CLIENT DISCONNECT
                self.__active = False
                self.__socket.shutdown(socket.SHUT_RDWR)
                self.__socket.close()
                del self.__socket, self.__qri
                # END
                self.__lock.release()
                raise
            self.__lock.acquire()
            if not self.__active:
                self.__thread = False
                self.__lock.release()
                break
            self.__lock.release()

    def __worker(self, ID, obj):
        'Reply to queries.'
        normal_query, name = obj[:2]
        if normal_query:
            # SECTION W1
            found, named_object = self.__find(name)
            if found:
                self.__exe(ID, named_object, *obj[2:])
            else:
                self.__qri.reply(ID, (False, AttributeError(name)))
        else:
            # SECTION W2
            if name == 'title':
                self.__qri.reply(ID, (True, self.__title))
            elif name == 'name':
                self.__qri.reply(ID, (True, self.__name))
            elif name == 'documentation':
                self.__qri.reply(ID, (True, self.__documentation))
            elif name == 'objects':
                self.__qri.reply(ID, (True, sorted(self.__objects.keys())))
            elif name == 'signature':
                self.__reply_signature(ID, obj[2])
            elif name == 'help':
                self.__reply_help(ID, obj[2])
            else:
                self.__qri.reply(ID, (False, NotImplementedError(name)))

    # SECTION W1

    def __exe(self, ID, obj, args, kwargs):
        'Execute an object and return the results.'
        try:
            self.__sync_lock.acquire()              # DEBUG
            sync = self.__syncronized               # DEBUG
            self.__sync_lock.release()              # DEBUG
            if sync:                                # DEBUG
                data = obj(*args, **kwargs)         # DEBUG
                import time; time.sleep(0.000001)   # DEBUG
                self.__qri.reply(ID, (True, data))  # DEBUG
            else:                                   # DEBUG
                self.__qri.reply(ID, (True, obj(*args, **kwargs)))
        except Exception, error:
            self.__qri.reply(ID, (False, error))
